# Server endpoints specification

### `/user/get/{user_id}`

*GET*

**Response**:
```json
{
	"name": *,
	"carbon_cost": *,
	"carbon_offset": *
}
```

The `carbon_cost` and `carbon_offset` provided here could be incorrect *if* there are concurrent transactions. For the working example, however, they will be working correctly to give the lifetime values.

### `/transaction/get/{transaction_id}`

*GET*

e.g. `transaction/get/12`

**Response**:
```json
{
	"price": *,
	"carbon_cost_offset": *,
	"vendor": *,
	"timestamp": *,
	"products":
	[
		{
			"company_name": *,
			"product_name": *,
		},
		{
			...
		},
		...
	]
}
```
### `/transaction/get_recent/{user_id}/{num_of_days}`

*GET*

e.g. `transaction/get_recent/9/7`

if the `{num_of_days}` field is 0, then get the lifetime data.

**Response**:
```json
{
	"carbon_cost": *,
	"carbon_offset": *,
	"transactions":
	[
		{
			"transaction_id": *,
			"price": *,
			"carbon_cost_offset": *,
			"vendor": *,
			"timestamp": *
		},
		{
			...
		},
		...
	]
}
```
Here `carbon_cost_offset` would be negative for an offsetting transaction.

### `/offset/get`

*GET*

**Response**:
```json
[
	{
		"vendor_id": *,
		"vendor": *,
		"description": *,
		"price": *
	},
	...
]
```
This is a list of the different offsetting options.

### `/offset/offset`

*POST*

**Request**:
```json
{
	"user_id": *
	"vendor_id": *,
	"offset_amount": *,
}
```
Here, `offset_amount` is the amount of carbon being offset.

**Response**:
```json
{
	"transaction_id": *,
	"price": *,
	"carbon_cost_offset": *,
	"vendor": *,
	"timestamp": *
}
```
If `transaction_id` is 0, then that means that the offsetting transaction has failed, and all other fields are undefined. Here, `carbon_cost_offset` would always be negative.

### `/transaction/update`

*POST*

**Request**:
```json
{
	"transaction_id": *,
	"carbon_cost_offset": *
}
```

**Response**:
```json
{
	"success": true/false
}
```
Carbon offsetting transactions may NOT be updated, hence `carbon_cost_offset` would always be positive.

### `/transaction/update_products`

*POST*

**Request**:
```json
{
	"transaction_id": *,
	"products":
	[
		{
			"company_id": *,
			"product_id": *
		},
		...
	]
}
```

**Response**:
```json
{
	"success": true/false
}
```

