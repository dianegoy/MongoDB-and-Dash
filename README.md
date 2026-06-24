# CS 340 Project Two: Grazioso Salvare Animal Shelter Dashboard

**Diane Goy | Professor Reed Perkins | June 2026**

---

## About the Project

This project is a reusable Python module with methods to create, read, update, 
and delete records in a MongoDB database. It is part of a full-stack application 
built for Grazioso Salvare, a rescue-animal training company that works with 
shelters to identify dogs that are good candidates for search-and-rescue training.

The module, `AnimalShelter`, connects to a MongoDB database called `aac` and 
exposes Python methods that other scripts can import and call. This separates 
database logic from application logic, making the code easier to test, maintain, 
and extend.

Project Two extends this foundation with a fully interactive web dashboard built 
using the Dash framework.

---

## Motivation

Grazioso Salvare needs a software application that can identify and categorize 
dogs from animal shelters as candidates for search-and-rescue training. The 
organization wanted the solution to be open-source so that other animal rescue 
groups can replicate it.

---

## Getting Started

### Database Setup

The Austin Animal Center Outcomes (aac) dataset was imported into MongoDB using 
the mongoimport tool. The database is named `aac` and the collection is `animals`.

```bash
mongoimport --type=csv --headerline --db aac --collection animals --drop ./aac_shelter_outcomes.csv
```

### User Authentication

For MongoDB, it is recommended to create a dedicated user and avoid using the 
admin account. To add a user with read and write privileges:

```javascript
use admin
db.createUser({
    user: 'aacuser',
    pwd: passwordPrompt(),
    roles: [{role: 'readWrite', db: 'aac'}]
})
```

> **Note:** The password is hardcoded for this assignment.

### The Python Module

The `AnimalShelter` class is defined in `CRUD_Python_Module.py`. Four methods 
were implemented: `create()`, `read()`, `update()`, and `delete()`, corresponding 
to the four standard database operations against the `animals` collection.

---

## Installation

| Tool | Purpose |
|---|---|
| Codio | Browser-based virtual lab provided by SNHU, preconfigured with required tools |
| MongoDB | Database used to store and query animal shelter data |
| Python 3 | Language used to write the CRUD module |
| PyMongo | Official Python driver for MongoDB; provides direct access to CRUD operations |
| Jupyter Notebook | Used to write and run the test script interactively |
| Dash | Python framework for building the interactive web dashboard |
| JupyterDash | Runs the Dash application inside a Jupyter Notebook environment |
| Dash Leaflet | Interactive geolocation mapping component |
| Plotly Express | Used for pie chart and data visualization |

---

## Usage

Import and instantiate the class, then call `create()`, `read()`, `update()`, 
or `delete()`:

```python
from CRUD_Python_Module import AnimalShelter
shelter = AnimalShelter()

# Create a record
shelter.create({
    "breed": "Basenji",
    "animal_type": "Dog",
    "name": "TestDog",
    "sex_upon_outcome": "Male",
    "age_upon_outcome": "3 years",
    "outcome_type": "Adoption"
})

# Read records matching a query
query = {'breed': 'Basenji'}
results = shelter.read(query)
print(results)

# Update a record
shelter.update({"name": "TestDog"}, {"$set": {"name": "NewTestDog"}})

# Delete a record
shelter.delete({"name": "NewTestDog"})
```

---

## Dashboard

The second phase adds a fully interactive web dashboard built with the Dash 
framework. The dashboard connects to MongoDB through the `AnimalShelter` CRUD 
module and allows Grazioso Salvare staff to filter, visualize, and interact with 
shelter animal data in real time. The dashboard is branded with the Grazioso 
Salvare logo, linked to [www.snhu.edu](http://www.snhu.edu), and includes a 
unique identifier crediting the developer.

### Widgets

- **Radio filter buttons** to filter by rescue type: Water Rescue, Mountain or 
  Wilderness Rescue, Disaster or Individual Tracking, and Reset
- **Interactive data table** that dynamically responds to the selected filter, 
  with pagination, sorting, and row selection
- **Pie chart** showing breed breakdown of animals currently displayed in the table
- **Geolocation map** that updates to show the location of the selected animal

### Tools and Rationale

MongoDB was chosen as the model component because it stores data as flexible 
JSON-like documents, which maps naturally to Python dictionaries and integrates 
cleanly with PyMongo. This makes it straightforward to pass query results directly 
into a Pandas DataFrame without additional transformation.

The Dash framework was chosen for the view and controller components because it 
allows Python developers to build interactive web dashboards without writing 
JavaScript. Dash combines Plotly for charts, Dash Leaflet for geolocation mapping, 
and a callback system that automatically updates components when inputs change. 
This MVC-style structure keeps database logic, visual components, and interaction 
logic clearly separated.

### Steps Taken

1. Imported `CRUD_Python_Module` so the dashboard had database functionality
2. Connected to MongoDB using the `AnimalShelter` class and loaded all records 
   into a Pandas DataFrame
3. Built the dashboard layout including the banner image, unique identifier, radio 
   filter buttons, and data table
4. Built filter queries based on the Dashboard Specifications Document
5. Implemented the filter callback to query the database and update the data table 
   when a radio button is selected
6. Added the pie chart using Plotly Express

### Challenges

**Constructor mismatch:** The CRUD module was written with no parameters, while 
the dashboard starter code passed username and password as arguments. Resolved by 
calling `AnimalShelter()` with no arguments and relying on hardcoded credentials 
inside the class.

**Map IndexError:** The map callback threw an `IndexError` when switching filters 
because the previously selected row no longer existed in the filtered dataset. 
Resolved by adding guards to check for empty data and reset the row index to zero 
when out of range.

**Pie chart scope:** The pie chart initially displayed all records from the 
unfiltered DataFrame instead of the currently filtered data. Resolved by switching 
the chart input from the original `df` to the `dff` variable derived from 
`derived_virtual_data`. Labels were also clipped by displaying only the top ten 
breeds and grouping the remainder as "Other."

---

## Reflections

### How do you write programs that are maintainable, readable, and adaptable?

Writing maintainable code comes down to separation of concerns. Building the CRUD 
module as a standalone class meant the database logic lived in one place. When the 
dashboard needed to query animals by rescue type, there was no need to rewrite 
connection logic or relearn the database structure. The dashboard just imported 
the class and called `read()`. That kind of encapsulation makes the code easier 
to test in isolation, easier to update if the database changes, and easier for 
someone else to pick up.

The `AnimalShelter` module could be reused in any other Python application that 
needs to interact with that database. A command-line reporting tool, a REST API, 
or a second dashboard for a different department could all import the same class 
without touching the underlying connection code.

### How do you approach a problem as a computer scientist?

For this project, the starting point was the client's actual need: Grazioso 
Salvare needed a way to filter animals by rescue type and see results visually. 
Working backward from that, the database had to be structured and queryable in a 
way that supported those filters, and the dashboard had to surface the right 
information without requiring the user to know anything about MongoDB.

Compared to earlier coursework, this project required thinking about how 
components interact across layers. It was not just writing a function that 
produces an output but designing a system where a database, a Python class, and a 
web interface all work together consistently. For future projects, starting with 
the client's filtering and reporting needs before touching any code is something 
I would carry forward, along with building the data layer first so application 
logic has something reliable to build on.

### What do computer scientists do, and why does it matter?

Computer scientists translate real-world problems into systems that can process, 
organize, and surface information at a scale that would not be practical otherwise. 
For a company like Grazioso Salvare, manually reviewing shelter records to find 
dogs with the right age, breed, and training profile for a specific rescue type 
would take significant time and introduce human error. The dashboard makes that 
process nearly instant and repeatable.

More broadly, the same pattern applies anywhere organizations are sitting on data 
they cannot easily act on. Building tools that connect a database to a clear, 
usable interface turns raw records into something staff can actually use to make 
decisions.

---

## License

Open source, intended for replication by other animal rescue organizations.
