## Run the Project Locally

### Clone the repository:  
```git clone https://github.com/dikshasa17/car-accident-website.git```

### CD into the project:  
```cd car-accident-website```

### Install virtual env using (ignore if already installed on the system) :
```pip install virtualenv```

### Make virtual environment using:
``` virtualenv venv```

### To enable running scripts on system (Type it in powershell as an administrator)
```Set-ExecutionPolicy Unrestricted```

### Activate virtual environment:  
```.\venv\Scripts\activate```

### Install requirements.txt:  
```pip install -r requirements.txt```

### Create a new db.sqlite3 database if needed to store users

### In view.py write your firebase configuration lines

### In firebase create Realtime and Storage database which has read and write permission for anyone (ignore if already done)

### In Realtime database rules, mention the nodes you create and the subnodes on which index should be on (ignore if already done)

### To run the project:
```python manage.py runserver```