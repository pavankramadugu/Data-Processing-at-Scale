def FindBusinessBasedOnCity(cityToSearch, saveLocation1, collection):
    business_docs = collection.filter(lambda obj: obj['city'] == cityToSearch)
    with open(saveLocation1, "w") as file:
        for business in business_docs:
            name = business['name']
            full_address = business['full_address'].replace("\n", ", ")
            city = business['city']
            state = business['state']
            file.write(name + "$" + full_address + "$" + city + "$" + state + "\n")


def FindBusinessBasedOnLocation(categoriesToSearch, myLocation, maxDistance, saveLocation2, collection):
    business_docs = collection.filter(lambda obj: set(categoriesToSearch).issubset(set(obj['categories'])))
    lat1 = float(myLocation[0])
    lon1 = float(myLocation[1])
    with open(saveLocation2, "w") as file:
        for business in business_docs:
            name = business['name']
            lat2 = float(business['latitude'])
            lon2 = float(business['longitude'])
            d = DistanceFunction(lat2, lon2, lat1, lon1)
            if d <= maxDistance:
                file.write(name + "\n")
