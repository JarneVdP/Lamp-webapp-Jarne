# Lamps webapp using Flask

## Run the project
```
python -m lamps
```
Use `-m` to run the whole application

## Database
The database won't work yet. From your starting location, where lamps.py is located, run
```
python -m app.main.manage-db
```
Now in the main folder, database.db will be created. The database will store the accounts. They are created automatically.

## Browser location
When everything is configured, it will run at `localhost:8080/`. 

## Docker
A dockerfile has also been added. You can build it using 
```
docker build –t <containername>:<tag> <path>
e.g. sudo docker build -t jarnevdp/lamps:latest .
```
After that run
```
sudo docker run --name <name> -it --rm --network=host <containername>:<tag>:..
e.g. sudo docker run --name lampss -it --rm --network=host jarnevdp/lamps:latest 
```
-it for an interactive terminal
--rm to remove container when it's done
--network=host, not needed except when you want it to run on your own network if you run on a vpn
