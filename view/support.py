import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from utils import check_date_format

console = Console()


class SupportMenu:
    @staticmethod
    def support_menu():
        console.print(Panel(
            "[bold green]1.[/bold green] Menu clients\n"
            "[bold green]2.[/bold green] Menu contrats\n"
            "[bold green]3.[/bold green] Menu événements\n"
            "[bold green]4.[/bold green] Quitter la session",
            title="[bold magenta]Menu Support[/bold magenta]",
            expand=False
        ))

    @staticmethod
    def support_customers_menu():
        console.print(Panel(
            "[bold green]1.[/bold green] Afficher toutes les fiches clients\n"
            "[bold green]2.[/bold green] Rechercher un client\n"
            "[bold green]3.[/bold green] Retour au menu support",
            title="[bold magenta]Menu Clients[/bold magenta]",
            expand=False
        ))

    @staticmethod
    def support_contrats_menu():
        console.print(Panel(
            "[bold green]1.[/bold green] Afficher tous les contrats\n"
            "[bold green]2.[/bold green] Rechercher un contrat\n"
            "[bold green]3.[/bold green] Retour au menu support",
            title="[bold magenta]Menu Contrats[/bold magenta]",
            expand=False
        ))

    @staticmethod
    def support_events_menu():
        console.print(Panel(
            "[bold green]1.[/bold green] Modifier un événement\n"
            "[bold green]2.[/bold green] Afficher tous les événements\n"
            "[bold green]3.[/bold green] Mes événements assignés\n"
            "[bold green]4.[/bold green] Rechercher un événement\n"
            "[bold green]5.[/bold green] Retour au menu support",
            title="[bold magenta]Menu Événements[/bold magenta]",
            expand=False
        ))


class SupportViews:
    @staticmethod
    def show_all_events_self_support(events):
        if not events:
            console.print("[bold red]❌ Vous n'êtes responsable d'aucun événement.[/bold red]")
            return

        table = Table(title="Événements Assignés", show_lines=True)
        table.add_column("ID", justify="center")
        table.add_column("Contrat", justify="center")
        table.add_column("Client", justify="left")
        table.add_column("Titre", justify="left")
        table.add_column("Début", justify="center")
        table.add_column("Fin", justify="center")
        table.add_column("Adresse", justify="left")

        for event in events:
            table.add_row(
                str(event.id),
                str(event.contract_id),
                event.contract.customer.name_lastname,
                event.title,
                str(event.date_hour_start),
                str(event.date_hour_end),
                event.address
            )

        console.print(table)

    @staticmethod
    def update_event_view_support(event, id):
        console.print(Panel(
            f"[bold magenta]Modifier l'événement N°{id}[/bold magenta]",
            expand=False
        ))
        title = Prompt.ask(
            f"[bold cyan]Titre de l'événement ({event.title})[/bold cyan]",
            default=event.title
        )
        date_hour_start = SupportViews.prompt_for_date(
            f"Date et heure du début ({event.date_hour_start})", event.date_hour_start
        )
        date_hour_end = SupportViews.prompt_for_date(
            f"Date et heure de fin ({event.date_hour_end})", event.date_hour_end
        )
        address = Prompt.ask(
            f"[bold cyan]Adresse ({event.address})[/bold cyan]",
            default=event.address
        )
        guests = Prompt.ask(
            f"[bold cyan]Nombre d'invités ({event.guests})[/bold cyan]",
            default=str(event.guests)
        )
        notes = Prompt.ask(
            f"[bold cyan]Notes ({event.notes})[/bold cyan]",
            default=event.notes
        )

        return title, date_hour_start, date_hour_end, address, int(guests), notes

    @staticmethod
    def not_assigned_event():
        console.print("[bold red]❌ Vous ne semblez être responsable d'aucun événement.[/bold red]")

    @staticmethod
    def prompt_for_date(prompt_text, default_value):
        # Convertir en chaîne si le défaut est un objet datetime
        if isinstance(default_value, datetime.datetime):
            default_value = default_value.strftime("%Y-%m-%d %H:%M:%S")
        while True:
            date_input = Prompt.ask(f"[bold cyan]{prompt_text}[/bold cyan]", default=default_value)
            if check_date_format(date_input):
                return date_input
            console.print("[bold red]❌ Format invalide. Veuillez entrer une date valide (AAAA-MM-JJ HH:MM:SS).[/bold red]")
