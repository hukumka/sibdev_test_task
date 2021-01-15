# Test assignment for sibdev

Web application for processing list of deals

## REST API entrypoints

### `/process_deals`

Submit list of deals for processing.

Method: POST

#### Arguments
- deals: csv file containing list of deals.


Csv file must contain header 
`customer, item, total, quantity, date`


Each row must contain columns:

- customer - Customers login. `string`
- item - Bought item. `string`
- total - Total value of the deal. `integer`
- quantity - Number of items bought. `integer`
- date - Date and time then deal was done. Must be in ISO8601 format.

#### Result

- Status Ok (On successful submission)
- Status Error, Desc = (Error description)

### `/get_processing_result`

Retrieves list of 5 most valuable customers, based on list of deals submitted with `/process_deals`.

Method: GET

#### Arguments

None

#### Result

```json5
{
    [
        "username": "username" // Username of customer
        "spent_money": "100" // Total amount of money spent by customer
        "gems": [ // List of gems bought by customer that also been bought by someone else in top 5.
            "gems1",
            ...
        ]
    ],
    ...
}
```

## Building and running

Requires: docker-compose

Clone repository and enter directory:

```
git clone https://github.com/hukumka/sibdev_test_task
cd sibdev_test_task
```

Build docker image:
```
docker-compose build
```

To run service execute command:

```
docker-compose up
```
