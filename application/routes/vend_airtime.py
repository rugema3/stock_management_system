from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app

from decorators.admin_decorators import admin_required

vend_airtime_route = Blueprint('vend_airtime', __name__)

@vend_airtime_route.route('/vend_airtime', methods=['GET', 'POST'])
@admin_required
def vend_airtime():
    """
    send airtime to different users.
    """
    # Retrieve the required instances
    db = current_app.db
    user_handler = current_app.user_handler
    airtime = current_app.airtime

    user_department = session.get('department')
    user_role = session.get('role')
    # Retrieve available PEI
    pei = user_handler.get_all_pei()
    ambassadors = user_handler.get_all_ambassadors()
    print(ambassadors)
    print()
    for name in ambassadors:
        print(f"Name: {name[1]} phone: {name[2]} PEI: {name[3]} amount: {name[4]} RWF")

    if request.method == 'POST':
        try:
            print("Try block accessible in post method.")
            print("the contents of the form: ", request.form.get('selection'))
            if 'customer_account_number' in request.form and 'local_currency' in request.form:
                print("sending airtime form.")
                # Get the user's input from the form
                customer_account_number = request.form['customer_account_number']
                local_currency = float(request.form['local_currency'])
                vertical_id = 'airtime'

                # Perform vend validation
                validate_response = airtime.vend_validate(vertical_id, customer_account_number)

                # Extract necessary information.
                trx_id = validate_response.get("data", {}).get("trxId", "")
                delivery_method = validate_response.get("data", {}).get("deliveryMethods", [{}])[0].get("id", "")
                deliver_to = validate_response.get("data", {}).get("deliverTo", "")
                callback = validate_response.get("data", {}).get("callback", "")
                customer_name = validate_response.get("data", {}).get("customerAccountNumber", "")
                product_name = validate_response.get("data", {}).get("pdtName", "")

                # Perform vend execution with the retrieved information
                try:
                    execute_response = airtime.vend_execute(
                        trx_id,
                        customer_account_number,
                        local_currency,
                        vertical_id,
                        delivery_method,
                        deliver_to,
                        callback)
                    flash("sending airtime is successful. ", execute_response)
                    print("Sucessfully sent airtime. ", execute_response)
                except Exception as e:
                    print("Failed to send airtime. ", e)

            elif 'pei_name' in request.form and 'amount' not in request.form and 'name' not in request.form:
                print("Inside the pei form.")
                pei_name = request.form['pei_name']
                print()
                print("pei Name is: ", pei_name)
                # Insert the pei name in the database.
                try:
                    insert = user_handler.add_pei(pei_name)
                    flash("PEI has been added successfully.")
                    return redirect(url_for('vend_airtime.vend_airtime'))
                except Exception as e:
                    error_message = f'Failed to add PEI: {str(e)}'
                    flash(error_message, 'error')

            elif 'name' in request.form: 
                name = request.form['name']
                phone = request.form['phone']
                pei = request.form['pei_name']
                amount = request.form['amount']
                try:
                    success = user_handler.add_ambassador(name, phone, pei, amount)
                    message = f"{name} with phone: {phone} at {pei} has been added to receive {amount} RWF of airtime."
                    flash(message)
                    return redirect(url_for('vend_airtime.vend_airtime'))
                except Exception as e:
                    flash("something went wrong while adding a member. Please try again or contact the IT Department if the issue persists.")
                    return redirect(url_for('vend_airtime.vend_airtime'))

            elif 'yes' in request.form.get('selection'):
                for ambassador in ambassadors:
                    amount = float(ambassador[4])
                    print("amount: ", amount)
                    phone = ambassador[2]
                    print("Phone: ", phone)
                    vertical_id = 'airtime'

                    try:
                        # Perform vend validation
                        validate_response = airtime.vend_validate(
                                vertical_id, 
                                phone
                                )
                        # Extract necessary information.
                        trx_id = validate_response.get("data", {}).get("trxId", "")
                        delivery_method = validate_response.get("data", {}).get("deliveryMethods", [{}])[0].get("id", "")
                        deliver_to = validate_response.get("data", {}).get("deliverTo", "")
                        callback = validate_response.get("data", {}).get("callback", "")
                        customer_name = validate_response.get("data", {}).get("customerAccountNumber", "")
                        product_name = validate_response.get("data", {}).get("pdtName", "")

                        # Perform vend execution with the retrieved information
                        try:
                            execute_response = airtime.vend_execute(
                                trx_id,
                                phone,
                                amount,
                                vertical_id,
                                delivery_method,
                                deliver_to,
                                callback)
                            flash("sending airtime is successful. ", execute_response)
                            print("Sucessfully sent airtime. ", execute_response)
                        except Exception as e:
                            print("Failed to send airtime. ", e)

                    except Exception as e:
                        print("Validating the tranbsaction failed.: ", e)

        except Exception as e:
            flash(f'Error: {str(e)}', 'error')

    # Render the template with the available departments
    return render_template(
            'vend_airtime.html', 
            user_department=user_department, 
            user_role=user_role,
            pei=pei,
            ambassadors=ambassadors
            )

