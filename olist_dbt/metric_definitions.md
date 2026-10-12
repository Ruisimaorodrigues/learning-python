# Olist Metric Definitions

## 1. Total Revenue (BRL)
**Definition:** Sum of payment_value across all delivered orders.
**Assumptions:**
- Only orders with order_status = 'delivered' are included
- Cancelled, processing and other statuses are excluded
- Currency: Brazilian Reais (BRL)
- Date used: order_purchase_timestamp (not delivery date)
- Multiple payments per order are summed

## 2. Total Orders
**Definition:** Count of unique order_ids with status = 'delivered'.
**Assumptions:**
- One order = one unique order_id
- Cancelled orders are excluded
- Orders with missing payment data are still counted

## 3. Average Days to Deliver
**Definition:** Average number of days between order_purchase_timestamp and order_delivered_customer_date.
**Assumptions:**
- Only delivered orders with a valid delivery date are included
- Negative values (data errors) are excluded
- Calculated in calendar days, not business days
- Timezone: UTC

## 4. Revenue per State (BRL)
**Definition:** Sum of payment_value grouped by customer_state.
**Assumptions:**
- State is determined by customer billing address, not delivery address
- Same exclusions as Total Revenue

## 5. Average Order Value (BRL)
**Definition:** Total Revenue / Total Orders.
**Assumptions:**
- Calculated as: sum(payment_value) / count(distinct order_id)
- Only delivered orders
- Excludes orders with zero payment value

## 6. Freight Rate
**Definition:** Total freight value as a percentage of total items value.
**Formula:** sum(freight_value) / sum(price) * 100
**Assumptions:**
- Only delivered orders
- Expressed as a percentage
- Orders with zero items value are excluded to avoid division by zero