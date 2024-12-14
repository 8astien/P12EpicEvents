from model import User, Customer, Contract, Event
from view.management import (
    ManagementMenu, ManagementUserViews,
    ManagementContractViews, ManagementEventViews,
    ManagementSearchViews
)
from view.principal import MainView, MainSearch


class ManagementController(ManagementMenu):
    def __init__(self, user):
        while True:
            ManagementMenu.management_menu()
            choice = MainView.choice()
            if not choice.isdigit() or not 1 <= int(choice) <= 5:
                MainView.message_no_whole_number()
                continue
            try:
                handle_management_choice(int(choice), user)
            except Exception as e:
                print(f"Erreur : {e}")


def handle_management_choice(choice, user):
    try:
        if choice == 1:
            handle_user_management()
        elif choice == 2:
            handle_customer_management()
        elif choice == 3:
            handle_contract_management()
        elif choice == 4:
            handle_event_management()
        elif choice == 5:
            exit()
    except Exception as e:
        print(f"Erreur : {e}")


def handle_user_management():
    while True:
        ManagementMenu.management_users_menu()
        choice = MainView.choice()
        if not choice.isdigit() or not 1 <= int(choice) <= 6:
            MainView.message_no_whole_number()
            continue

        choice = int(choice)
        try:
            if choice == 1:  # Créer un collaborateur
                name_lastname, department, password, email = ManagementUserViews.create_user_view()
                User.create(
                    name_lastname=name_lastname,
                    department=department,
                    password=password,
                    email=email
                )
                ManagementUserViews.validation_user_creation(name_lastname)
            elif choice == 2:  # Modifier un collaborateur
                id_ = ManagementUserViews.update_user_id_view()
                user = User.find_by_id(id_)
                if user:
                    name_lastname, department, password, email = ManagementUserViews.update_user_view(user)
                    user.update(
                        user,
                        name_lastname=name_lastname,
                        department=department,
                        password=password,
                        email=email
                    )
                    ManagementUserViews.validation_update_user_view(user)
                else:
                    ManagementUserViews.none_user_view()
            elif choice == 3:  # Supprimer un collaborateur
                id_ = ManagementUserViews.delete_user_id_view()
                user = User.find_by_id(id_)
                if user:
                    ManagementUserViews.confirmation_delete_user_view(user)
                    if MainView.oui_non_input():
                        user.delete(user)
                        ManagementUserViews.validation_delete_user_view(user)
                    else:
                        ManagementUserViews.cancelation_delete_user_view()
                else:
                    ManagementUserViews.none_user_view()
            elif choice == 4:  # Rechercher un collaborateur par ID
                id_ = MainSearch.search_all_users_search()
                user = User.find_by_id(id_)
                if user:
                    MainSearch.show_all_users([user])
                else:
                    MainView.message_no_user_whith_search()
            elif choice == 5:  # Afficher tous les collaborateurs
                users = User.find_all()
                if users:
                    MainSearch.show_all_users(users)
                else:
                    MainView.message_no_user()
            elif choice == 6:  # Retour au menu principal
                return
        except Exception as e:
            print(f"Erreur : {e}")


def handle_customer_management():
    while True:
        ManagementMenu.management_customers_menu()
        choice = MainView.choice()
        if not choice.isdigit() or not 1 <= int(choice) <= 3:
            MainView.message_no_whole_number()
            continue

        choice = int(choice)
        try:
            if choice == 1:  # Afficher tous les clients
                customers = Customer.find_all()
                if customers:
                    MainSearch.show_all_customers(customers)
                else:
                    MainView.message_no_customer()
            elif choice == 2:  # Rechercher un client par ID
                id_ = MainSearch.search_all_customers_search()
                customer = Customer.find_by_id(id_)
                if customer:
                    MainSearch.show_all_customers([customer])
                else:
                    MainView.message_no_customer_whith_search()
            elif choice == 3:  # Retour au menu principal
                return
        except Exception as e:
            print(f"Erreur : {e}")


def handle_contract_management():
    while True:
        ManagementMenu.management_contrats_menu()
        choice = MainView.choice()
        if not choice.isdigit() or not 1 <= int(choice) <= 5:
            MainView.message_no_whole_number()
            continue

        choice = int(choice)
        try:
            if choice == 1:  # Créer un contrat
                id_ = ManagementContractViews.create_contract_id_customer_view()
                customer = Customer.find_by_id(id_)
                if customer:
                    ManagementContractViews.confirmation_create_contract_view(customer)
                    if MainView.oui_non_input():
                        total_amount, settled_amount, contract_sign = ManagementContractViews.create_contract_view()
                        Contract.create(
                            customer_id=customer.id,
                            total_amount=total_amount,
                            settled_amount=settled_amount,
                            contract_sign=contract_sign
                        )
                        ManagementContractViews.validation_create_contract_view()
                    else:
                        ManagementContractViews.cancelation_create_contract_view()
                else:
                    ManagementContractViews.none_customer_view()
            elif choice == 2:  # Modifier un contrat
                id_ = ManagementContractViews.update_contract_id_view()
                contract = Contract.find_by_id(id_)
                if contract:
                    total_amount,
                    settled_amount,
                    contract_sign = ManagementContractViews.update_contract_view(contract, id_)
                    contract.update(
                        contract,
                        total_amount=total_amount,
                        settled_amount=settled_amount,
                        contract_sign=contract_sign
                    )
                    ManagementContractViews.validation_update_contract_view()
                else:
                    ManagementContractViews.none_contract_view()
            elif choice == 3:  # Afficher tous les contrats
                contracts = Contract.find_all()
                if contracts:
                    MainSearch.show_all_contracts(contracts)
                else:
                    MainView.message_no_contract()
            elif choice == 4:  # Rechercher un contrat par ID
                id_ = MainSearch.search_all_contracts_search()
                contract = Contract.find_by_id(id_)
                if contract:
                    MainSearch.show_all_contracts([contract])
                else:
                    MainView.message_no_contract_whith_search()
            elif choice == 5:  # Retour au menu principal
                return
        except Exception as e:
            print(f"Erreur : {e}")


def handle_event_management():
    while True:
        ManagementMenu.management_events_menu()
        choice = MainView.choice()
        if not choice.isdigit() or not 1 <= int(choice) <= 5:
            MainView.message_no_whole_number()
            continue

        choice = int(choice)
        try:
            if choice == 1:  # Modifier un événement
                id_ = ManagementEventViews.update_event_id_contract_view()
                event = Event.find_by_id(id_)
                if event:
                    title, date_hour_start, date_hour_end, address, guests, notes, support_id = ManagementEventViews.update_event_view(
                        event, id_)
                    event.update(
                        event,
                        title=title,
                        date_hour_start=date_hour_start,
                        date_hour_end=date_hour_end,
                        address=address,
                        guests=guests,
                        notes=notes,
                        support_contact=support_id
                    )
                    ManagementEventViews.validation_update_event_view()
                else:
                    ManagementEventViews.none_event_view()
            elif choice == 2:  # Afficher tous les événements
                events = Event.find_all()
                if events:
                    MainSearch.show_all_events(events)
                else:
                    MainView.message_no_event()
            elif choice == 3:  # Rechercher un événement par ID
                id_ = MainSearch.search_all_events_search()
                event = Event.find_by_id(id_)
                if event:
                    MainSearch.show_all_events([event])
                else:
                    MainView.message_no_event_whith_search()
            elif choice == 4:  # Afficher les événements sans support
                events = Event.find_events_without_support()
                if events:
                    ManagementSearchViews.show_all_events_no_support()
                else:
                    ManagementEventViews.all_event_assigned()
            elif choice == 5:  # Retour au menu principal
                return
        except Exception as e:
            print(f"Erreur : {e}")
