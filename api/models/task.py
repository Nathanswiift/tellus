from tellus import Database as db

class Task:
    @classmethod
    def one(cls):
        response = db.select_all("""
        SELECT C.CustomerId, C.FirstName, C.LastName, GROUP_CONCAT(P.Number separator ',') as PhoneNumbers, 
        (SELECT Count(*) FROM CustomerRental WHERE CustomerId = C.CustomerId) as timesRented,
        (SELECT max(RentFrom) FROM CustomerRental WHERE CustomerId = C.CustomerId) as latestRent,
        (SELECT min(RentFrom) FROM CustomerRental WHERE CustomerId = C.CustomerId) as FirstRent
        FROM(SELECT CustomerId, FirstName, LastName, PhoneId 
        FROM Customer
        JOIN CustomerPhone USING(CustomerId)
        JOIN Phone USING(PhoneId)
        WHERE CustomerId IN(SELECT CustomerId FROM CustomerPhone GROUP BY CustomerId HAVING count(CustomerId) > 1)
        and PhoneType = 'Cell') as C
        INNER JOIN CustomerPhone CP ON CP.CustomerId = C.CustomerId
        INNER JOIN Phone P ON P.PhoneId = CP.PhoneId
        GROUP By C.CustomerId
        """
        )
        arr = []
        for row in response:
            arr.append(
                {
                    "CustomerId": row[0],
                    "FirstName": row[1],
                    "LastName": row[2],
                    "Numbers": row[3],
                    "TimesRented": row[4],
                    "LatestRent": str(row[5]),
                    "FirstRent": str(row[6])
                },
            )
        return arr

    @classmethod
    def two(cls):
        response = db.select_all("""
        WITH Counter(CarId, Times)
        as
        (
            SELECT CustomerRental.CarId, count(*) as times FROM CustomerRental
            INNER JOIN Car ON Car.CarId = CustomerRental.CarId
            GROUP BY CustomerRental.CarId
        )

        SELECT Car.CarId, Car.Milage, Car.RegistrationNumber, Color.ColorName, CarModel.CarType, CarModel.ModelName, 
        ifnull(max(CustomerRental.RentFrom), 'Never Rented') as RentedFrom, ifnull(max(CustomerRental.RentTo), 'Never Rented') as RentedTo,
        ifnull(Counter.Times, 0) as TotalTimesRented
        FROM Car
        INNER JOIN Color ON Color.ColorId = Car.ColorId
        INNER JOIN CarModel ON Car.ModelId = CarModel.CarModelId
        LEFT JOIN CustomerRental ON Car.CarId = CustomerRental.CarId
        LEFT JOIN Counter ON Car.CarId = Counter.CarId
        WHERE Color.ColorName = 'Blue'
        AND 
        Car.CarId NOT IN(SELECT CarId FROM CustomerRental WHERE RentFrom BETWEEN '2013-03-10' AND '2013-03-21' OR RentTo Between '2013-03-10' AND '2013-03-21')
        GROUP BY Car.CarId
        """
        )
        arr = []
        for row in response:
            arr.append(
                {
                    "CarId": row[0],
                    "Milage": row[1],
                    "RegistrationNumber": row[2],
                    "Color": row[3],
                    "CarType": row[4],
                    "Model": row[5],
                    "RentedFrom": row[6],
                    "RentedTo": row[7],
                    "TotalTimesRented": row[8]
                }
            )
        return arr