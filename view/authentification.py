from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
import pyperclip

console = Console()


class AuthentificationMenu:
    @staticmethod
    def main_authentification_menu():
        console.print(Panel(
            "[bold green]1.[/bold green] Générer un nouveau token d'accès\n"
            "[bold green]2.[/bold green] Me connecter avec un token existant\n"
            "[bold green]3.[/bold green] Quitter l'application\n",
            title="[bold magenta]Authentification[/bold magenta]",
            expand=False
        ))


class AuthenticationViews:
    @staticmethod
    def token_creation():
        console.print(Panel(
            "[bold yellow]ATTENTION :[/bold yellow] Générer un nouveau token remplacera le précédent !",
            title="[bold red]Avertissement[/bold red]",
            expand=False
        ))
        name_lastname = Prompt.ask("[bold cyan]Entrez votre nom complet[/bold cyan]")
        password = Prompt.ask("[bold cyan]Entrez votre mot de passe[/bold cyan]", password=True)
        return name_lastname, password

    @staticmethod
    def token_print(encoded_jwt):
        console.print(Panel(
            "[bold green]🎉 Token généré avec succès ![/bold green]\n\n"
            "✅ [bold cyan]Votre token est unique et sécurisé.[/bold cyan]\n"
            "🔒 Veillez à le conserver en lieu sûr et à ne jamais le partager.\n"
            "📅 Ce token sera valide pendant 48 heures.\n\n"
            "[bold cyan]Voici votre token :[/bold cyan]",
            title="[bold magenta]Token généré[/bold magenta]",
            expand=False
        ))
        console.print(f"[bold yellow]{encoded_jwt}[/bold yellow]")

        # Copier automatiquement dans le presse-papiers
        try:
            pyperclip.copy(encoded_jwt)
            console.print("\n[bold green]💾 Le token a été copié automatiquement dans votre presse-papiers ![/bold green]")
        except pyperclip.PyperclipException:
            console.print(
                "\n[bold red]❌ Impossible de copier le token dans le presse-papiers. Veuillez le copier manuellement.[/bold red]")

    @staticmethod
    def error_authentication():
        console.print(Panel(
            "[bold red]Erreur : Identifiant ou mot de passe incorrect.[/bold red]\n\n"
            "Vérifiez vos informations et essayez à nouveau.",
            title="[bold red]Échec de l'authentification[/bold red]",
            expand=False
        ))

    @staticmethod
    def token_cheking():
        console.print(Panel(
            "[bold cyan]Connexion avec un token existant[/bold cyan]\n"
            "Collez ou entrez votre token pour continuer.",
            title="[bold magenta]Authentification[/bold magenta]",
            expand=False
        ))
        token = Prompt.ask("[bold cyan]Entrez votre token[/bold cyan]")
        return token

    @staticmethod
    def expiration_date_token():
        console.print(Panel(
            "[bold yellow]⏳ Votre token a expiré.[/bold yellow]\n\n"
            "Veuillez générer un nouveau token pour continuer.",
            title="[bold red]Token expiré[/bold red]",
            expand=False
        ))

    @staticmethod
    def invalid_token():
        console.print(Panel(
            "[bold red]❌ Token invalide.[/bold red]\n\n"
            "Assurez-vous que le token est correct et réessayez.",
            title="[bold red]Erreur de token[/bold red]",
            expand=False
        ))
