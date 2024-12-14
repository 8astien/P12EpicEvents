from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from utils import check_date_format
from database import session
from model.user import User
from model.event import Event
from datetime import datetime

console = Console()

# Menu Management


class ManagementMenu:
    @staticmethod
    def management_menu():
        console.print(Panel(
            "[bold green]1.[/bold green] Menu Collaborateurs\n"
            "[bold green]2.[/bold green] Menu Clients\n"
            "[bold green]3.[/bold green] Menu Contrats\n"
            "[bold green]4.[/bold green] Menu Événements\n"
            "[bold green]5.[/bold green] Quitter la session",
            title="[bold magenta]Menu Gestion[/bold magenta]",
            expand=False
        ))

    @staticmethod
    def management_users_menu():
        console.print(Panel(
            "[bold green]1.[/bold green] Créer un collaborateur\n"
            "[bold green]2.[/bold green] Modifier un collaborateur\n"
            "[bold green]3.[/bold green] Supprimer un collaborateur\n"
            "[bold green]4.[/bold green] Rechercher un collaborateur\n"
            "[bold green]5.[/bold green] Afficher tous les collaborateurs\n"
            "[bold green]6.[/bold green] Retour au menu gestion",
            title="[bold magenta]Menu Collaborateurs[/bold magenta]",
            expand=False
        ))

    @staticmethod
    def management_customers_menu():
        console.print(Panel(
            "[bold green]1.[/bold green] Afficher toutes les fiches clients\n"
            "[bold green]2.[/bold green] Rechercher un client\n"
            "[bold green]3.[/bold green] Retour au menu gestion",
            title="[bold magenta]Menu Clients[/bold magenta]",
            expand=False
        ))

    @staticmethod
    def management_contrats_menu():
        console.print(Panel(
            "[bold green]1.[/bold green] Créer un contrat\n"
            "[bold green]2.[/bold green] Modifier un contrat\n"
            "[bold green]3.[/bold green] Afficher tous les contrats\n"
            "[bold green]4.[/bold green] Rechercher un contrat\n"
            "[bold green]5.[/bold green] Retour au menu gestion",
            title="[bold magenta]Menu Contrats[/bold magenta]",
            expand=False
        ))

    @staticmethod
    def management_events_menu():
        console.print(Panel(
            "[bold green]1.[/bold green] Modifier un événement\n"
            "[bold green]2.[/bold green] Afficher tous les événements\n"
            "[bold green]3.[/bold green] Rechercher un événement\n"
            "[bold green]4.[/bold green] Afficher les événements sans support\n"
            "[bold green]5.[/bold green] Retour au menu gestion",
            title="[bold magenta]Menu Événements[/bold magenta]",
            expand=False
        ))


# Search Views
class ManagementSearchViews:
    @staticmethod
    def show_all_events_no_support():
        events = Event.find_events_without_support()
        if not events:
            console.print("[bold yellow]Tous les événements ont un support associé.[/bold yellow]")
            return

        table = Table(title="Événements sans support associé")
        table.add_column("ID")
        table.add_column("Contrat ID")
        table.add_column("Client")
        table.add_column("Date début")
        table.add_column("Date fin")
        table.add_column("Adresse")
        table.add_column("Invités")

        for event in events:
            table.add_row(
                str(event.id),
                str(event.contract_id),
                event.contract.customer.name_lastname,
                str(event.date_hour_start),
                str(event.date_hour_end),
                event.address,
                str(event.guests)
            )
        console.print(table)


# User Management
class ManagementUserViews:

    @staticmethod
    def create_user_view():
        console.print(Panel(
            "[bold cyan]Créer un nouveau collaborateur[/bold cyan]",
            title="[bold magenta]Nouveau Collaborateur[/bold magenta]",
            expand=False
        ))
        name_lastname = Prompt.ask("[bold cyan]Nom et prénom[/bold cyan]")
        department = ManagementUserViews.prompt_for_department()

        # garantir un mot de passe valide
        while True:
            password = Prompt.ask("[bold cyan]Mot de passe[/bold cyan]")
            if password.strip():
                break
            console.print("[bold red]❌ Le mot de passe ne peut pas être vide. Veuillez réessayer.[/bold red]")

        email = Prompt.ask("[bold cyan]Adresse email[/bold cyan]")
        return name_lastname, department, password, email

    @staticmethod
    def prompt_for_department():
        while True:
            department = Prompt.ask(
                "[bold cyan]Département (COM: Commercial, GES: Gestion, SUP: Support)[/bold cyan]"
            ).upper()
            if department in ["COM", "GES", "SUP"]:
                return department
            console.print("[bold red]❌ Département invalide. Choisissez parmi COM, GES, ou SUP.[/bold red]")

    @staticmethod
    def validation_user_creation(name_lastname):
        console.print(f"[bold green]🎉 Collaborateur {name_lastname} créé avec succès ![/bold green]")

    @staticmethod
    def delete_user_id_view():
        return Prompt.ask("[bold cyan]ID du collaborateur à supprimer[/bold cyan]")

    @staticmethod
    def confirmation_delete_user_view(user):
        return Prompt.ask(
            f"[bold red]Êtes-vous sûr de vouloir supprimer {user.name_lastname} ? (Oui/Non)[/bold red]"
        ).lower() == "oui"

    @staticmethod
    def validation_delete_user_view(user):
        console.print(f"[bold green]🎉 Collaborateur {user.name_lastname} supprimé avec succès ![/bold green]")

    @staticmethod
    def cancelation_delete_user_view():
        console.print("[bold yellow]❌ Suppression annulée.[/bold yellow]")

    @staticmethod
    def none_user_view():
        console.print("[bold red]❌ Aucun collaborateur trouvé avec cet ID.[/bold red]")

    @staticmethod
    def update_user_id_view():
        return Prompt.ask("[bold cyan]ID du collaborateur à modifier[/bold cyan]")

    @staticmethod
    def update_user_view(user):
        console.print(Panel(
            "[bold cyan]Modifier un collaborateur[/bold cyan]",
            title=f"[bold magenta]Collaborateur N°{user.id}[/bold magenta]",
            expand=False
        ))
        name_lastname = Prompt.ask(
            f"[bold cyan]Nom et prénom [/bold cyan]",
            default=user.name_lastname
        )
        department = ManagementUserViews.prompt_for_department()
        password = Prompt.ask(
            "[bold cyan]Mot de passe (laissez vide pour ne pas modifier)[/bold cyan]"
        )
        email = Prompt.ask(
            f"[bold cyan]Adresse email [/bold cyan]",
            default=user.email
        )
        return name_lastname, department, password, email

    @staticmethod
    def validation_update_user_view(user):
        console.print(f"[bold green]🎉 Collaborateur {user.name_lastname} modifié avec succès ![/bold green]")


# Contract Management
class ManagementContractViews:
    @staticmethod
    def create_contract_id_customer_view():
        console.print(Panel(
            "[bold cyan]À partir de quel client souhaitez-vous créer un contrat ?[/bold cyan]",
            title="[bold magenta]Création de contrat[/bold magenta]",
            expand=False
        ))
        return Prompt.ask("[bold cyan]ID du client[/bold cyan]")

    @staticmethod
    def create_contract_view():
        console.print(Panel(
            "[bold cyan]Veuillez renseigner les informations du contrat[/bold cyan]",
            title="[bold magenta]Nouveau Contrat[/bold magenta]",
            expand=False
        ))
        total_amount = Prompt.ask("[bold cyan]Coût total du contrat[/bold cyan]", default="0", show_default=True)
        settled_amount = Prompt.ask("[bold cyan]Montant déjà réglé[/bold cyan]", default="0", show_default=True)
        contract_sign = Prompt.ask(
            "[bold cyan]Le contrat a-t-il été validé par le client ? (Oui/Non)[/bold cyan]").lower()
        return int(total_amount), int(settled_amount), contract_sign == "oui"

    @staticmethod
    def validation_create_contract_view():
        console.print("[bold green]🎉 Votre contrat a été créé avec succès ![/bold green]")

    @staticmethod
    def cancelation_create_contract_view():
        console.print("[bold yellow]❌ Création annulée.[/bold yellow]")

    @staticmethod
    def none_customer_view():
        console.print("[bold red]❌ Aucun client trouvé avec cet ID.[/bold red]")

    @staticmethod
    def confirmation_create_contract_view(customer):
        console.print(Panel(
            f"[bold cyan]Souhaitez-vous créer un contrat pour le client [bold magenta]{customer.name_lastname}[/bold magenta] ?[/bold cyan]",
            title="[bold magenta]Confirmation[/bold magenta]",
            expand=False
        ))
        return Prompt.ask("[bold cyan]Confirmez (Oui/Non)[/bold cyan]").lower() == "oui"

    @staticmethod
    def update_contract_id_view():
        console.print(Panel(
            "[bold cyan]Quel contrat souhaitez-vous modifier ?[/bold cyan]",
            title="[bold magenta]Modification de contrat[/bold magenta]",
            expand=False
        ))
        return Prompt.ask("[bold cyan]ID du contrat[/bold cyan]")

    @staticmethod
    def update_contract_view(contract, id):
        console.print(Panel(
            f"[bold cyan]Modification du contrat [bold magenta]N°{id}[/bold magenta][/bold cyan]",
            title="[bold magenta]Mise à jour[/bold magenta]",
            expand=False
        ))
        total_amount = Prompt.ask(
            f"[bold cyan]Coût total du contrat (actuel : {contract.total_amount})[/bold cyan]",
            default=str(contract.total_amount)
        )
        settled_amount = Prompt.ask(
            f"[bold cyan]Montant déjà réglé (actuel : {contract.settled_amount})[/bold cyan]",
            default=str(contract.settled_amount)
        )
        contract_sign = Prompt.ask(
            f"[bold cyan]Le contrat a-t-il été validé ? (actuel : {'Oui' if contract.contract_sign else 'Non'})[/bold cyan]",
            default="Oui" if contract.contract_sign else "Non"
        ).lower()
        return float(total_amount), float(settled_amount), contract_sign == "oui"

    @staticmethod
    def validation_update_contract_view():
        console.print("[bold green]🎉 Votre contrat a été modifié avec succès ![/bold green]")

    @staticmethod
    def none_contract_view():
        console.print("[bold red]❌ Aucun contrat trouvé avec cet ID.[/bold red]")

    @staticmethod
    def not_in_charge_contract_view():
        console.print("[bold red]❌ Vous n'êtes pas responsable de ce contrat.[/bold red]")


# Events Management
class ManagementEventViews:
    @staticmethod
    def create_event_id_contract_view():
        console.print(Panel(
            "[bold cyan]À partir de quel contrat souhaitez-vous créer un événement ?[/bold cyan]",
            title="[bold magenta]Création d'événement[/bold magenta]",
            expand=False
        ))
        return Prompt.ask("[bold cyan]ID du contrat[/bold cyan]")

    @staticmethod
    def confirmation_create_event_view(contract):
        console.print(Panel(
            f"[bold cyan]Souhaitez-vous créer un événement pour le client [bold magenta]{contract.customer.name_lastname}[/bold magenta] "
            f"à partir du contrat [bold magenta]N°{contract.id}[/bold magenta] ?[/bold cyan]",
            title="[bold magenta]Confirmation[/bold magenta]",
            expand=False
        ))
        return Prompt.ask("[bold cyan]Confirmez (Oui/Non)[/bold cyan]").lower() == "oui"

    @staticmethod
    def create_event_view():
        console.print(Panel(
            "[bold cyan]Veuillez renseigner les informations de l'événement[/bold cyan]",
            title="[bold magenta]Nouvel événement[/bold magenta]",
            expand=False
        ))

        title = Prompt.ask("[bold cyan]Nom de l'événement[/bold cyan]")

        date_hour_start = ManagementEventViews._ask_date(
            "[bold cyan]Date et heure de début (AAAA-MM-JJ HH:MM:SS)[/bold cyan]"
        )
        date_hour_end = ManagementEventViews._ask_date(
            "[bold cyan]Date et heure de fin (AAAA-MM-JJ HH:MM:SS)[/bold cyan]"
        )

        address = Prompt.ask("[bold cyan]Adresse de l'événement[/bold cyan]")
        guests = int(Prompt.ask("[bold cyan]Nombre d'invités (0 par défaut)[/bold cyan]", default="0"))
        notes = Prompt.ask("[bold cyan]Notes (optionnel)[/bold cyan]", default="")

        return title, date_hour_start, date_hour_end, address, guests, notes, None

    @staticmethod
    def validation_create_event_view():
        console.print("[bold green]🎉 Votre événement a été créé avec succès ![/bold green]")

    @staticmethod
    def cancelation_create_event_view():
        console.print("[bold yellow]❌ Création annulée.[/bold yellow]")

    @staticmethod
    def not_sign_contract_view(contract):
        console.print(Panel(
            f"[bold red]❌ Le contrat [bold magenta]N°{contract.id}[/bold magenta] n'a pas été signé par le client. "
            f"Veuillez prendre contact avec ce dernier.[/bold red]",
            title="[bold red]Contrat non signé[/bold red]",
            expand=False
        ))

    @staticmethod
    def none_event_view():
        console.print("[bold red]❌ Aucun événement trouvé avec cet ID.[/bold red]")

    @staticmethod
    def update_event_id_contract_view():
        console.print(Panel(
            "[bold cyan]Quel événement souhaitez-vous modifier ?[/bold cyan]",
            title="[bold magenta]Modification d'événement[/bold magenta]",
            expand=False
        ))
        return Prompt.ask("[bold cyan]ID de l'événement[/bold cyan]")

    @staticmethod
    def update_event_view(event, id):
        console.print(Panel(
            f"[bold cyan]Modification de l'événement [bold magenta]N°{id}[/bold magenta][/bold cyan]",
            title="[bold magenta]Mise à jour[/bold magenta]",
            expand=False
        ))

        title = Prompt.ask(f"[bold cyan]Nom de l'événement (actuel : {event.title})[/bold cyan]", default=event.title)

        # Convertir les dates actuelles en chaînes
        default_start = event.date_hour_start.strftime("%Y-%m-%d %H:%M:%S") if event.date_hour_start else None
        default_end = event.date_hour_end.strftime("%Y-%m-%d %H:%M:%S") if event.date_hour_end else None

        date_hour_start = ManagementEventViews._ask_date(
            f"[bold cyan]Date et heure de début (actuel : {default_start})[/bold cyan]",
            default=default_start
        )
        date_hour_end = ManagementEventViews._ask_date(
            f"[bold cyan]Date et heure de fin (actuel : {default_end})[/bold cyan]",
            default=default_end
        )

        address = Prompt.ask(f"[bold cyan]Adresse (actuelle : {event.address})[/bold cyan]", default=event.address)
        guests = int(Prompt.ask(
            f"[bold cyan]Nombre d'invités (actuel : {event.guests})[/bold cyan]", default=str(event.guests)))
        notes = Prompt.ask(f"[bold cyan]Notes (actuelles : {event.notes})[/bold cyan]", default=event.notes)

        # Ajouter la gestion du support_contact
        support_id = None
        if event.support_contact:
            support_id = int(Prompt.ask(
                f"[bold cyan]ID du support associé (actuel : {event.support_contact})[/bold cyan]",
                default=str(event.support_contact)
            ))
        else:
            support_id = int(Prompt.ask(
                "[bold cyan]ID du support associé (aucun pour l'instant)[/bold cyan]", default="0"))

        return title, date_hour_start, date_hour_end, address, guests, notes, support_id

    @staticmethod
    def validation_update_event_view():
        console.print("[bold green]🎉 Votre événement a été modifié avec succès ![/bold green]")

    @staticmethod
    def not_in_charge_event_view():
        console.print("[bold red]❌ Vous n'êtes pas responsable de cet événement.[/bold red]")

    @staticmethod
    def all_event_assigned():
        console.print("[bold green]✅ Tous les événements ont été assignés à des responsables.[/bold green]")

    @staticmethod
    def _ask_date(prompt_message, default=None):
        while True:
            date_input = Prompt.ask(prompt_message, default=default)
            if check_date_format(date_input):
                return date_input
            console.print("[bold red]❌ Format invalide. Veuillez utiliser le format AAAA-MM-JJ HH:MM:SS.[/bold red]")

    @staticmethod
    def validation_update_event_view():
        console.print("[bold green]🎉 Votre événement a été modifié avec succès ![/bold green]")
