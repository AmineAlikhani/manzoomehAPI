### Creating API end-points using Manzoomeh Basis Core
### How to run ?
#1# Clone the repository :
```bash
> git clone https://github.com/abolfazlj00/Manzoomeh-basis-core.git
```
#2# Create a virtualenv and activate it:
# on GNU Linux cmd : 
```bash
> pyton -m venv .venv
> source venv\bin\activate
```
#3# Install the requirements :
```bash
> pip install -r requirements.txt
```
#4# Run project
# On this repository cmd: 
```bash
> pyton api.py
```
### Available end-points:
#http://127.0.0.1:8080/api/
#http://127.0.0.1:8080/api/<int:product_id>
#http://127.0.0.1:8080/api/delete/<int:product_id>
#http://127.0.0.1:8080/api/add/<product_info>
#http://127.0.0.1:8080/api/edit/<int:product_id>/<product_info>

