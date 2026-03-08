from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from matrimony.models import Candidate, AdminProfile
from datetime import date, timedelta


class Command(BaseCommand):
    help = 'Send daily notification emails to admins'

    def handle(self, *args, **kwargs):
        today = date.today()
        
        # New entries today
        new_candidates = Candidate.objects.filter(created_at__date=today, is_paid=True).select_related('rasi', 'nachathiram', 'profession')
        
        # Expired premium entries
        expired_candidates = Candidate.objects.filter(premium_end_date__lt=today, is_paid=True, status='active').select_related('rasi', 'nachathiram')

        admins = User.objects.filter(is_staff=True).exclude(email='')
        admin_emails = list(admins.values_list('email', flat=True))

        if not admin_emails:
            self.stdout.write('No admin emails found.')
            return

        # Send new entries email
        if new_candidates.exists():
            subject = f'செம்போடையார் - இன்றைய புதிய விண்ணப்பங்கள் ({today.strftime("%d/%m/%Y")})'
            rows = ""
            for c in new_candidates:
                rows += f"""
                <tr>
                    <td>{c.uid}</td>
                    <td>{c.name}</td>
                    <td>{'ஆண்' if c.gender == 'M' else 'பெண்'}</td>
                    <td>{c.age}</td>
                    <td>{c.rasi}</td>
                    <td>{c.nachathiram}</td>
                    <td>{c.profession}</td>
                    <td>{c.monthly_salary or '-'}</td>
                    <td>{c.educational_qualification}</td>
                </tr>"""
            html = f"""
            <html><body style="font-family: Arial; direction: ltr;">
            <h2 style="color:#b91c1c;">செம்போடையார் வன்னியர் திருமண மையம்</h2>
            <h3>இன்றைய புதிய விண்ணப்பங்கள் - {today.strftime("%d/%m/%Y")}</h3>
            <table border="1" cellpadding="8" style="border-collapse:collapse;width:100%">
            <tr style="background:#fef2f2"><th>UID</th><th>பெயர்</th><th>பாலினம்</th><th>வயது</th><th>ராசி</th><th>நட்சத்திரம்</th><th>தொழில்</th><th>சம்பளம்</th><th>கல்வி</th></tr>
            {rows}
            </table></body></html>"""
            send_mail(subject, '', 'noreply@sembodai.com', admin_emails, html_message=html, fail_silently=True)
            self.stdout.write(f'Sent new entries email: {new_candidates.count()} entries')

        # Send expiry notification
        if expired_candidates.exists():
            subject = f'செம்போடையார் - காலாவதியான விண்ணப்பங்கள் ({today.strftime("%d/%m/%Y")})'
            rows = ""
            for c in expired_candidates:
                rows += f"""
                <tr>
                    <td>{c.uid}</td>
                    <td>{c.name}</td>
                    <td>{c.premium_end_date.strftime("%d/%m/%Y")}</td>
                    <td>{c.created_by}</td>
                </tr>"""
            html = f"""
            <html><body style="font-family: Arial;">
            <h2 style="color:#b91c1c;">செம்போடையார் வன்னியர் திருமண மையம்</h2>
            <h3>⚠️ காலாவதியான பிரீமியம் விண்ணப்பங்கள்</h3>
            <table border="1" cellpadding="8" style="border-collapse:collapse;width:100%">
            <tr style="background:#fef2f2"><th>UID</th><th>பெயர்</th><th>முடிவு தேதி</th><th>சேர்த்தவர்</th></tr>
            {rows}
            </table>
            <p>தயவுசெய்து விண்ணப்பதாரர்களை தொடர்பு கொண்டு புதுப்பிக்கவும்.</p>
            </body></html>"""
            send_mail(subject, '', 'noreply@sembodai.com', admin_emails, html_message=html, fail_silently=True)
            self.stdout.write(f'Sent expiry email: {expired_candidates.count()} entries')
