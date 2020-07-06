# My Toolbox

One toolbox for all my needs.

## Installation
Download latest .whl from releases.
```
pip install <release>.whl
```

## Features

### Dependencies

- Supports mvnrepository.com only
- Can save deps details to local database

#### Search
- by query term
```
box deps search ktor
```
- by group id and artifact id 
```
box deps search --group io.ktor --artifact ktor-client-core
or
box deps search -g io.ktor -a ktor-client-core
```

#### List saved deps with latest version
```
box deps list
```