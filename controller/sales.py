from view.management import ManagementContractViews, ManagementEventViews, ManagementSearchViews
from view.sales import SalesMenu, SalesCustomerViews, SalesSearchViews
from view.principal import MainView, MainSearch
from model import Customer, Contract, Event


class SalesController:
    def __init__(self, user):
        while True:
            try:
                SalesMenu.sale_menu()
                choice = MainView.choice()
                if choice.isdigit() and 1 <= int(choice) <= 4:
                    handle_sales_choice(int(choice), user)
                else:
                    MainView.message_no_whole_number()
            except Exception as e:
                print(f"Erreur : {e}")


def handle_sales_choice(choice, user):
    try:
        if choice == 1:
            handle_customer_management(user)
        elif choice == 2:
            handle_contract_management(user)
        elif choice == 3:
            handle_event_management(user)
        elif choice == 4:
            exit()
    except Exception as e:
        print(f"Erreur : {e}")


def handle_customer_management(user):
    while True:
        try:
            SalesMenu.sale_customers_menu()
            choice = MainView.choice()
            if choice.isdigit() and 1 <= int(choice) <= 6:
                choice = int(choice)
                if choice == 1:
                    name_lastname, email, phone, business_name = SalesCustomerViews.create_customer_view()
                    Customer.create(
                        name_lastname=name_lastname,
                        email=email,
                        phone=phone,
                        business_name=business_name,
                        sales_contact=user.id
                    )
                    SalesCustomerViews.validation_customer_creation()
                elif choice == 2:
                    id_ = SalesCustomerViews.update_customer_id_view()
                    customer = Customer.find_by_id(id_)
                    if customer and customer.sales_contact == user.id:
                        name_lastname, email, phone, business_name = SalesCustomerViews.update_customer_view(customer)
                        customer.update(
                            customer,
                            name_lastname=name_lastname or customer.name_lastname,
                            email=email or customer.email,
                            phone=phone or customer.phone,
                            business_name=business_name or customer.business_name
                        )
                        SalesCustomerViews.validation_update_customer_view()
                    elif customer:
                        SalesCustomerViews.not_in_charge_customer_view()
                    else:
                        SalesCustomerViews.none_customer_view()
                elif choice == 3:
                    customers = Customer.find_all()
                    MainSearch.show_all_customers(customers) if customers else MainView.message_no_customer()
                elif choice == 4:
                    search = MainSearch.search_all_customers_search()  # Demander l'ID
                    customer = Customer.find_by_id(search)  # Recherche par ID
                    if customer:
                        MainSearch.show_all_customers([customer])
                    else:
                        MainView.message_no_customer_whith_search()
                elif choice == 5:
                    customers = Customer.find_by_sales_contact(user.id)
                    SalesSearchViews.show_my_customers(
                        customers) if customers else SalesCustomerViews.no_customers_found()
                elif choice == 6:
                    return
            else:
                MainView.message_no_whole_number()
        except Exception as e:
            print(f"Erreur : {e}")


def handle_contract_management(user):
    while True:
        try:
            SalesMenu.sale_contracts_menu()
            choice = MainView.choice()
            if choice.isdigit() and 1 <= int(choice) <= 7:
                choice = int(choice)
                if choice == 1:
                    id_ = ManagementContractViews.update_contract_id_view()
                    contract = Contract.find_by_id(id_)
                    if contract and contract.customer.sales_contact == user.id:
                        total_amount, settled_amount, contract_sign = ManagementContractViews.update_contract_view(
                            contract, id_)
                        contract.update(
                            contract,
                            total_amount=total_amount,
                            settled_amount=settled_amount,
                            contract_sign=contract_sign
                        )
                        ManagementContractViews.validation_update_contract_view()
                    elif contract:
                        SalesCustomerViews.not_in_charge_customer_view()
                    else:
                        ManagementContractViews.none_contract_view()
                elif choice == 2:
                    contracts = Contract.find_by_sales_contact(user.id)
                    MainSearch.show_all_contracts(contracts) if contracts else MainView.message_no_contract()
                elif choice == 3:
                    contracts = Contract.find_by_sales_contact(user.id)
                    SalesSearchViews.show_my_contracts(
                        contracts) if contracts else SalesCustomerViews.no_contract_view()
                elif choice == 4:
                    contracts = [c for c in Contract.find_by_sales_contact(user.id) if not c.contract_sign]
                    SalesSearchViews.show_my_contracts_not_sign(
                        contracts) if contracts else SalesCustomerViews.all_contract_sign_view()
                elif choice == 5:
                    contracts = [c for c in Contract.find_by_sales_contact(user.id) if c.remaining_amount > 0]
                    SalesSearchViews.show_my_contracts_remaining_amount(
                        contracts) if contracts else SalesCustomerViews.all_contract_settled()
                elif choice == 6:
                    search = MainSearch.search_all_contracts_search()  # Demande l'ID du contrat
                    contract = Contract.find_by_id(search)  # Recherche par ID
                    if contract and contract.customer.sales_contact == user.id:  # Vérifie si l'utilisateur est le commercial responsable
                        # Passe le contrat trouvé dans une liste pour l'affichage
                        MainSearch.show_all_contracts([contract])
                    elif contract:
                        SalesCustomerViews.not_in_charge_customer_view()  # Message si non responsable
                    else:
                        MainView.message_no_contract_whith_search()
                elif choice == 7:
                    return
            else:
                MainView.message_no_whole_number()
        except Exception as e:
            print(f"Erreur : {e}")


def handle_event_management(user):
    while True:
        try:
            SalesMenu.sale_events_menu()  # Menu spécifique aux événements
            choice = MainView.choice()
            if choice.isdigit() and 1 <= int(choice) <= 5:
                choice = int(choice)
                if choice == 1:  # Créer un événement
                    contract_id = ManagementEventViews.create_event_id_contract_view()
                    contract = Contract.find_by_id(contract_id)
                    if contract and contract.customer.sales_contact == user.id and contract.contract_sign:
                        # Demander les détails de l'événement
                        title, date_hour_start, date_hour_end, address, guests, notes, support_id = ManagementEventViews.create_event_view()
                        Event.create(
                            contract_id=contract.id,
                            title=title,
                            date_hour_start=date_hour_start,
                            date_hour_end=date_hour_end,
                            address=address,
                            guests=guests,
                            notes=notes,
                            support_contact=None  # Support sera attribué par le gestionnaire
                        )
                        ManagementEventViews.validation_create_event_view()
                    elif contract and not contract.contract_sign:
                        ManagementEventViews.not_sign_contract_view(contract)
                    else:
                        ManagementEventViews.none_event_view()
                elif choice == 2:
                    events = Event.find_all()
                    MainSearch.show_all_events(events) if events else MainView.message_no_event()
                elif choice == 3:
                    search = MainSearch.search_all_events_search()
                    event = Event.find_by_id(search)
                    MainSearch.show_all_events([event]) if event else MainView.message_no_event_whith_search()
                elif choice == 4:
                    return
            else:
                MainView.message_no_whole_number()
        except Exception as e:
            print(f"Erreur : {e}")
