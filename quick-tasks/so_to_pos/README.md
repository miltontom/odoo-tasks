This task consists method of creating pos orders from sales module and transfer it into the POS module
Add a Button Pay at the Counter Inside Sale order view.
Add a pos session field in the other Info Tab (default value of session opened by the responsible login)

Pay at the counter button opens a wizard - one2many field (values of
corresponding payment methods from pos),total amount paid,paid
amount,remaining amount
once the amount is fully paid pay at the counter button goes invisible

need a state' paid at the counter' in sale order which behaves exactly
as cancelled,once the pos order is created the sale order will go to
this state
The order lines from sale order will reflect to the
order lines in pos order and the payments from the wizard will reflect
to the payment tab in pos.
