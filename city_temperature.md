#CityTemperature
* CityTemperature Object
```
{
  city: string
  temperature: int
  timedelta: int
}
```
**REPORT /city**
----
  Returns current temperature of the city.
* **URL Params**
  *Required:* `city=[str] local_time=[int]`
* **Data Params**
  None
* **Headers**
  Content-Type: application/json
* **Success Response:** 
* **Code:** 200
  **Content:**
```
{
  CityTemperature:
           {<CityTemperature_object},
}
``` 
* **Error Response:**
  * **Code:** 400
  **Content:** `{ error : "Invalid input" }`
  OR
  * **Code:** 404
  **Content:** `{ error : "Not Found" }`
  OR
  * **Code:** 500
  **Content:** `{ error : "Internal error" }`

#CapitalCityTemperature
* CapitalCityTemperature Object
```
{
  city: string
  temperature: int
  timedelta: int
}
```
**REPORT /country**
----
  Returns current temperature of the capital city.
* **URL Params**
  *Required:* `country=[str] local_time=[int]`
* **Data Params**
  None
* **Headers**
  Content-Type: application/json
* **Success Response:** 
* **Code:** 200
  **Content:**
```
{
  CityTemperature:
           {<CityTemperature_object},
}
``` 
* **Error Response:**
  * **Code:** 400
  **Content:** `{ error : "Invalid input" }`
  OR
  * **Code:** 404
  **Content:** `{ error : "Not Found" }`
  OR
  * **Code:** 500
  **Content:** `{ error : "Internal error" }`
