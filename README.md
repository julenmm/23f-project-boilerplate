# Lodgistix

Lodgistix is a full-stack application for hotel chain management. Lodgistix allows hotel employees to search, add, delete, and change employee information, as well as fetch information for customers and their preferences. The backend consists of a number of RESTful API endpoints implemented using Python and Flask. These endpoints connect to a database using MySQL, a relational database management system. The front end is a web app implemented with Appsmith, a drag-and-drop UI editor.

Through Lodgistix Front Desk Agents have the ability to add new customers, delete old customers, retrieve customer information, update customer information, and fetch all room information.

Hotel Managers will have the capability to get all customer and employee information, add and delete employee information, as well as get and change employee shifts. 

Lastly, Housekeeping Supervisors will have the potential to view room, supply, employee, and shift status, as well as add new shifts, update time off requests, and change room status.

This app was created to explore how a relational database could be integrated into an application. We’ve created six web pages that represent the core functionality of the product.

## Screenshots

The Homepage

![Homepage](./screenshots/textbook_listing.png)

Front Fesk Agent

![Front Desk Agent](./screenshots/textbook_listing.png)

The Hotel Manager

=======
This app was created to explore how a relational database could be integrated into an application. We’ve created six web pages that represent the core functionality of the product.

## Screenshots

The Homepage

![Homepage](./screenshots/textbook_search.png)

Front Fesk Agent

![Front Desk Agent](./screenshots/textbook_listing.png)

The Hotel Manager

>>>>>>> 40cd6d00a8e0a80717e4596c8ddb53a233f34e24
![Hotel Manager](./screenshots/rating.png)

The Hotel Manager

![Hotel Manager](./screenshots/manage_listings.png)

The Housekeeping supervisor

![Housekeeping Supervisor](./screenshots/manage_listings.png)

The Housekeeping Supervisor

![Housekeeping Supervisor](./screenshots/manage_listings.png)

# Installation

To run Lodgistix, follow these steps:

1. Clone this repository
2. Create a file named `db_root_password.txt` in the `secrets/` folder, and put inside of it the root password for MySQL.
3. Create a file named `db_password.txt` in the `secrets/` folder, and put inside of it the password you want to use for the a non-root user named webapp.
4. In a terminal or command prompt, navigate to the folder with the docker-compose.yml file.
5. Build the images with docker compose build
6. Start the containers with `docker compose up`. To run in detached mode, run docker `compose up -d`. This starts three containers: the MySQL database, The Python Flask application, and the front end Appsmith application
7. The application will now be running on your local machine at http://localhost:8080.

For development, Install Python 3 and Flask using pip, the Python package manager, by running `pip install flask`

# Conclusion

Lodgistix is a simple application for managing all hotel resources, implemented using Python, Flask, and MySQL. The application provides RESTful API endpoints for managing employees, customers, and supplies, with the inclusion of error handling and logging for enhanced reliability and troubleshooting. If you have any questions or need further assistance, please refer to the documentation or contact the application administrator.
