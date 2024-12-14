from view.management import ManagementEventViews
from view.principal import MainView, MainSearch
from view.support import SupportMenu, SupportViews
from model import Event, Customer, Contract


class SupportController:
    def __init__(self, user):
        while True:
            try:
                SupportMenu.support_menu()
                choice = MainView.choice()
                if choice.isdigit() and 1 <= int(choice) <= 4:
                    handle_support_choice(int(choice), user)
                else:
                    MainView.message_no_whole_number()
            except Exception as e:
                print(f"Erreur : {e}")


def handle_support_choice(choice, user):
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
            SupportMenu.support_customers_menu()
            choice = MainView.choice()
            if choice.isdigit() and 1 <= int(choice) <= 3:
                choice = int(choice)
                if choice == 1:
                    customers = Customer.find_all()
                    MainSearch.show_all_customers(customers) if customers else MainView.message_no_customer()
                elif choice == 2:
                    search = MainSearch.search_all_customers_search()
                    customers = Customer.find_by_id(search)
                    MainSearch.show_all_customers_search(
                        [customers]) if customers else MainView.message_no_customer_whith_search()
                elif choice == 3:
                    return
            else:
                MainView.message_no_whole_number()
        except Exception as e:
            print(f"Erreur : {e}")


def handle_contract_management(user):
    while True:
        try:
            SupportMenu.support_contrats_menu()
            choice = MainView.choice()
            if choice.isdigit() and 1 <= int(choice) <= 3:
                choice = int(choice)
                if choice == 1:
                    contracts = Contract.find_all()
                    MainSearch.show_all_contracts(contracts) if contracts else MainView.message_no_contract()
                elif choice == 2:
                    search = MainSearch.search_all_contracts_search()
                    contracts = Contract.find_by_id(search)
                    MainSearch.show_all_contracts_search(
                        [contracts]) if contracts else MainView.message_no_contract_whith_search()
                elif choice == 3:
                    return
            else:
                MainView.message_no_whole_number()
        except Exception as e:
            print(f"Erreur : {e}")


def handle_event_management(user):
    while True:
        try:
            SupportMenu.support_events_menu()
            choice = MainView.choice()
            if choice.isdigit() and 1 <= int(choice) <= 5:
                choice = int(choice)
                if choice == 1:
                    id_ = ManagementEventViews.update_event_id_contract_view()
                    event = Event.find_by_id(id_)
                    if event and event.support_contact == user.id:
                        title, date_hour_start, date_hour_end, address, guests, notes = SupportViews.update_event_view_support(
                            event, id_)
                        event.update(
                            event,
                            title=title,
                            date_hour_start=date_hour_start,
                            date_hour_end=date_hour_end,
                            address=address,
                            guests=guests,
                            notes=notes
                        )
                        ManagementEventViews.validation_update_event_view()
                    elif event:
                        ManagementEventViews.not_in_charge_event_view()
                    else:
                        ManagementEventViews.none_event_view()
                elif choice == 2:
                    events = Event.find_all()
                    MainSearch.show_all_events(events) if events else MainView.message_no_event()
                elif choice == 3:
                    events = Event.find_by_support_contact(user.id)
                    SupportViews.show_all_events_self_support(events) if events else SupportViews.not_assigned_event()
                elif choice == 4:
                    search = MainSearch.search_all_events_search()
                    events = Event.find_by_id(search)
                    MainSearch.show_all_events_search([events]) if events else MainView.message_no_event_whith_search()
                elif choice == 5:
                    return
            else:
                MainView.message_no_whole_number()
        except Exception as e:
            print(f"Erreur : {e}")
