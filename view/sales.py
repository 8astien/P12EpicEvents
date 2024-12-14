from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

console = Console()


# This class is used to display different menus for the sales module
class SalesMenu:
    @staticmethod
    def sale_menu():
        console.print(Panel(
            "[bold green]1.[/bold green] Menu clients\n"
            "[bold green]2.[/bold green] Menu contrats\n"
            "[bold green]3.[/bold green] Menu événements\n"
            "[bold green]4.[/bold green] Quitter la session",
            title="[bold magenta]Menu Commercial[/bold magenta]",
            expand=False
        ))

    @staticmethod
    def sale_customers_menu():
        console.print(Panel(
            "[bold green]1.[/bold green] Créer une fiche client\n"
            "[bold green]2.[/bold green] Modifier une fiche client\n"
            "[bold green]3.[/bold green] Afficher toutes les fiches clients\n"
            "[bold green]4.[/bold green] Rechercher un client\n"
            "[bold green]5.[/bold green] Afficher mes clients\n"
            "[bold green]6.[/bold green] Retour au menu commercial",
            title="[bold magenta]Menu Clients[/bold magenta]",
            expand=False
        ))

    @staticmethod
    def sale_contracts_menu():
        console.print(Panel(
            "[bold green]1.[/bold green] Modifier un contrat\n"
            "[bold green]2.[/bold green] Afficher tous les contrats\n"
            "[bold green]3.[/bold green] Afficher mes contrats\n"
            "[bold green]4.[/bold green] Contrats non signés\n"
            "[bold green]5.[/bold green] Contrats non réglés\n"
            "[bold green]6.[/bold green] Rechercher un contrat\n"
            "[bold green]7.[/bold green] Retour au menu commercial",
            title="[bold magenta]Menu Contrats[/bold magenta]",
            expand=False
        ))

    @staticmethod
    def sale_events_menu():
        console.print(Panel(
            "[bold green]1.[/bold green] Créer un événement\n"
            "[bold green]2.[/bold green] Afficher tous les événements\n"
            "[bold green]3.[/bold green] Rechercher un événement\n"
            "[bold green]4.[/bold green] Retour au menu commercial",
            title="[bold magenta]Menu Événements[/bold magenta]",
            expand=False
        ))


# This class is used to display different search views for the sales module
class SalesSearchViews:
    @staticmethod
    def show_my_customers(customers):
        table = Table(title="Mes Clients", show_lines=True)
        table.add_column("ID", justify="center")
        table.add_column("Nom", justify="left")
        table.add_column("Email", justify="left")
        table.add_column("Téléphone", justify="center")
        table.add_column("Entreprise", justify="left")
        table.add_column("Dernière mise à jour", justify="center")

        for customer in customers:
            table.add_row(
                str(customer.id),
                customer.name_lastname,
                customer.email,
                str(customer.phone),
                customer.business_name,
                str(customer.last_date_update)
            )

        console.print(table)

    @staticmethod
    def show_my_contracts(contracts):
        table = Table(title="Mes Contrats", show_lines=True)
        table.add_column("ID", justify="center")
        table.add_column("Client", justify="left")
        table.add_column("Total", justify="center")
        table.add_column("Réglé", justify="center")
        table.add_column("Restant", justify="center")
        table.add_column("Signé", justify="center")

        for contract in contracts:
            table.add_row(
                str(contract.id),
                contract.customer.name_lastname,
                f"{contract.total_amount} €",
                f"{contract.settled_amount} €",
                f"{contract.remaining_amount} €",
                "✅" if contract.contract_sign else "❌"
            )

        console.print(table)

    @staticmethod
    def show_my_contracts_not_sign(contracts):
        console.print(Panel("[bold cyan]Mes Contrats Non Signés[/bold cyan]", expand=False))
        if contracts:
            SalesSearchViews.show_my_contracts(contracts)
        else:
            console.print("[bold red]Aucun contrat non signé trouvé.[/bold red]")

    @staticmethod
    def show_my_contracts_remaining_amount(contracts):
        console.print(Panel("[bold cyan]Mes Contrats Non Réglés[/bold cyan]", expand=False))
        if contracts:
            SalesSearchViews.show_my_contracts(contracts)
        else:
            console.print("[bold red]Aucun contrat non réglé trouvé.[/bold red]")

# This class is used to handle different views related to customers in the sales module


class SalesCustomerViews:
    @staticmethod
    def create_customer_view():
        console.print(Panel(
            "[bold magenta]Créer un nouveau client[/bold magenta]",
            expand=False
        ))
        name_lastname = Prompt.ask("[bold cyan]Nom et prénom du client[/bold cyan]")
        email = Prompt.ask("[bold cyan]Email du client[/bold cyan]")
        phone = Prompt.ask("[bold cyan]Téléphone du client[/bold cyan]")
        business_name = Prompt.ask("[bold cyan]Nom commercial du client[/bold cyan]")
        return name_lastname, email, int(phone), business_name

    @staticmethod
    def update_customer_view(customer):
        console.print(Panel(
            f"[bold magenta]Modifier le client N°{customer.id}[/bold magenta]",
            expand=False
        ))
        name_lastname = Prompt.ask(
            f"[bold cyan]Nom et prénom du client ({customer.name_lastname})[/bold cyan]",
            default=customer.name_lastname
        )
        email = Prompt.ask(
            f"[bold cyan]Email du client ({customer.email})[/bold cyan]",
            default=customer.email
        )
        phone = Prompt.ask(
            f"[bold cyan]Téléphone du client ({customer.phone})[/bold cyan]",
            default=str(customer.phone)
        )
        business_name = Prompt.ask(
            f"[bold cyan]Nom commercial du client ({customer.business_name})[/bold cyan]",
            default=customer.business_name
        )
        return name_lastname, email, int(phone), business_name

    @staticmethod
    def validation_customer_creation():
        console.print("[bold green]Client créé avec succès ![/bold green]")

    @staticmethod
    def update_customer_id_view():
        return Prompt.ask("[bold cyan]Entrez l'ID du client à modifier[/bold cyan]")

    @staticmethod
    def validation_update_customer_view():
        console.print("[bold green]Client mis à jour avec succès ![/bold green]")

    @staticmethod
    def not_in_charge_customer_view():
        console.print("[bold red]Vous n'êtes pas en charge de ce client.[/bold red]")

    @staticmethod
    def none_customer_view():
        console.print("[bold red]Aucun client trouvé avec cet ID.[/bold red]")

    @staticmethod
    def wrong_date_format():
        console.print("[bold red]Format de date incorrect. Réessayez.[/bold red]")
