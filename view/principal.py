from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

console = Console()


class MainSearch:
    @staticmethod
    def show_all_users(users):
        table = Table(title="Tous les Collaborateurs")
        table.add_column("ID", justify="center")
        table.add_column("Nom", justify="center")
        table.add_column("Département", justify="center")
        table.add_column("Email", justify="center")

        for user in users:
            table.add_row(str(user.id), user.name_lastname, user.department, user.email)

        console.print(table)

    @staticmethod
    def search_all_users_search():
        return Prompt.ask("[bold cyan]Recherche (ID)[/bold cyan]")

    @staticmethod
    def show_all_users_search(users):
        if users:
            MainSearch.show_all_users(users)
        else:
            console.print("[bold red]Aucun collaborateur trouvé avec cette recherche.[/bold red]")

    @staticmethod
    def show_all_customers(customers):
        table = Table(title="Tous les Clients")
        table.add_column("ID", justify="center")
        table.add_column("Nom", justify="center")
        table.add_column("Email", justify="center")
        table.add_column("Téléphone", justify="center")
        table.add_column("Nom d'entreprise", justify="center")
        table.add_column("Date de premier contact", justify="center")
        table.add_column("Dernière mise à jour", justify="center")
        table.add_column("Vendeur associé", justify="center")

        for customer in customers:
            # Convertir les objets datetime en chaînes de caractères
            date_first_contact = customer.date_first_contact.strftime(
                "%Y-%m-%d %H:%M:%S") if customer.date_first_contact else "Non spécifiée"
            last_date_update = customer.last_date_update.strftime(
                "%Y-%m-%d %H:%M:%S") if customer.last_date_update else "Non spécifiée"

            table.add_row(
                str(customer.id),
                customer.name_lastname,
                customer.email,
                str(customer.phone),
                customer.business_name,
                date_first_contact,
                last_date_update,
                customer.user.name_lastname if customer.user else "Aucun"
            )

        console.print(table)

    @staticmethod
    def search_all_customers_search():
        return Prompt.ask("[bold cyan]Recherche (ID)[/bold cyan]")

    @staticmethod
    def show_all_customers_search(customers):
        if customers:
            MainSearch.show_all_customers(customers)
        else:
            console.print("[bold red]Aucun client trouvé avec cette recherche.[/bold red]")

    @staticmethod
    def show_all_contracts(contracts):
        table = Table(title="Tous les Contrats")
        table.add_column("ID", justify="center")
        table.add_column("Client", justify="center")
        table.add_column("Email", justify="center")
        table.add_column("Téléphone", justify="center")
        table.add_column("Total", justify="center")
        table.add_column("Réglé", justify="center")
        table.add_column("Restant", justify="center")
        table.add_column("Date de création", justify="center")
        table.add_column("Signé", justify="center")
        table.add_column("Vendeur associé", justify="center")

        for contract in contracts:
            table.add_row(
                str(contract.id), contract.customer.name_lastname, contract.customer.email,
                contract.customer.phone, str(contract.total_amount),
                str(contract.settled_amount), str(contract.remaining_amount),
                str(contract.creation_date), str(contract.contract_sign),
                contract.customer.user.name_lastname
            )

        console.print(table)

    @staticmethod
    def search_all_contracts_search():
        return Prompt.ask("[bold cyan]Recherche (ID)[/bold cyan]")

    @staticmethod
    def show_all_contracts_search(contracts):
        if contracts:
            MainSearch.show_all_contracts(contracts)
        else:
            console.print("[bold red]Aucun contrat trouvé avec cette recherche.[/bold red]")

    @staticmethod
    def show_all_events(events):
        table = Table(title="Tous les Événements", show_lines=True)
        table.add_column("ID", justify="center")
        table.add_column("Contrat", justify="center")
        table.add_column("Client", justify="left")
        table.add_column("Nom de l'événement", justify="left")
        table.add_column("Début", justify="center")
        table.add_column("Fin", justify="center")
        table.add_column("Adresse", justify="left")
        table.add_column("Invités", justify="center")
        table.add_column("Notes", justify="left")
        table.add_column("Support", justify="left")

        for event in events:
            table.add_row(
                str(event.id),
                str(event.contract_id),
                event.contract.customer.name_lastname if event.contract else "N/A",
                event.title,
                event.date_hour_start.strftime(
                    "%Y-%m-%d %H:%M:%S") if isinstance(event.date_hour_start, datetime) else "N/A",
                event.date_hour_end.strftime(
                    "%Y-%m-%d %H:%M:%S") if isinstance(event.date_hour_end, datetime) else "N/A",
                event.address,
                str(event.guests),
                event.notes or "N/A",
                event.user.name_lastname if event.user else "Aucun"
            )

        console.print(table)

    @staticmethod
    def search_all_events_search():
        return Prompt.ask("[bold cyan]Recherche (ID)[/bold cyan]")

    @staticmethod
    def show_all_events_search(events):
        if events:
            MainSearch.show_all_events(events)
        else:
            console.print("[bold red]Aucun événement trouvé avec cette recherche.[/bold red]")


class MainView:
    @staticmethod
    def oui_non_input():
        response = Prompt.ask("[bold cyan]Êtes vous-sûr ?[/bold cyan]").strip().lower()
        return response in ["oui", "yes", "true"]

    @staticmethod
    def error_oui_non_input():
        console.print("[bold red]Erreur : veuillez répondre par 'Oui' ou 'Non'.[/bold red]")

    @staticmethod
    def choice():
        return Prompt.ask("[bold cyan]Votre choix[/bold cyan]")

    @staticmethod
    def message_connection_token():
        console.print("[bold green]Connexion réussie avec votre token.[/bold green]")

    @staticmethod
    def message_no_department():
        console.print("[bold red]Impossible de récupérer le département de l'utilisateur.[/bold red]")

    @staticmethod
    def message_no_whole_number():
        console.print("[bold red]Veuillez saisir un nombre entier ![/bold red]")

    @staticmethod
    def message_no_user():
        console.print("[bold red]Aucun utilisateur n'a été trouvé ![/bold red]")

    @staticmethod
    def message_no_customer():
        console.print("[bold red]Aucun client pour le moment.[/bold red]")

    @staticmethod
    def message_no_contract():
        console.print("[bold red]Aucun contrat pour le moment.[/bold red]")

    @staticmethod
    def message_no_event():
        console.print("[bold red]Aucun événement pour le moment.[/bold red]")

    @staticmethod
    def message_no_user_whith_search():
        console.print("[bold red]Aucun utilisateur associé à cet ID.[/bold red]")

    @staticmethod
    def message_no_contract_whith_search():
        console.print("[bold red]Aucun contrat associé à cet ID.[/bold red]")

    @staticmethod
    def message_no_event_whith_search():
        console.print("[bold red]Aucun évènement associé à cet ID.[/bold red]")
