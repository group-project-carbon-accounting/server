# Server endpoints specification

## Testing endpoints

### `/test/{test_val}

*GET*

**Response**: `{test_val}`

This is used to test the GET functionality, where the test value is echoed back plainly, not in a JSON format.

### `/test`

*POST*

**Request**:
```json
{
	"test": *
}
```

**Response**: `*`

This is used to test the POST functionality, where the test value is echoed back plainly, not in a JSON format.

## Payment endpoints

### `/payment/`

*POST*

**Request**:
```json
{
	"user_id": *,
	"vendor_id": *,
	"price": *,
	"carbon_cost": *,
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

Here, `price` is the monetary component of the transaction in cents, and `carbon_cost` is in units of carbon. 

The vendor bank can use either `products` list or the `carbon_cost` field. If both are provided, then `products` list takes precedence. If neither is provided, then the carbon cost is defaulted to 0.

## Company endpoints

### `/product/add`

*POST*

**Request**:
```json
{
	"company_id": *,
	"product_id": *,
	"carbon_cost_offset": *
}
```

**Response**:
```json
{
	"success": true/false
}
```

### `/product/update`

*POST*

**Request**:
```json
{
	"company_id": *,
	"product_id": *,
	"carbon_cost_offset": *
}
```

**Response**:
```json
{
	"success": true/false
}
```

### `/product/get/{company_id}/{product_id}

*GET*

**Response**:
```json
{
	"generic": true/false,
	"carbon_cost_offset": *
}
```

The `generic` attribute indicates whether the specific company’s carbon cost/offset for that product is stored and hence retrieved from the database or not. If it is false, a generic carbon cost/offset is used.

## App endpoints

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

Here, the values are given for the lifetime of the user’s account.

### `/transaction/get/{transaction_id}`

*GET*

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

The timestamp is being given in the format of *Sun, 05 Mar 2022, 20:36:57* and the all attributes contain the human-readable names rather than their identifier numbers. These apply to `get_recent` as well.

### `/transaction/get_recent/{user_id}/{num_of_days}`

*GET*

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

Here `carbon_cost_offset` would be negative for an offsetting transaction, and the `carbon_cost` and `carbon_offset` document the units of carbon in question during the queried timeframe.

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

Carbon offsetting transactions may NOT be updated, hence `carbon_cost_offset` must always be positive.

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

The carbon cost associated with this transaction will be recalculated based on the product list given.

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

The response would be the offset transaction with the `products` list removed. If `transaction_id` is 0, then that means that the offsetting transaction has failed, and all other fields are undefined.
