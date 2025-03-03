from typing import Union
import yagmail
import io


class ReportEmail:

    @staticmethod
    def email_report(
        from_email: str,
        email_password: str,
        to_email: str,
        subject: str,
        body: str,
        attachment: Union[str, io.IOBase],
    ) -> None:
        """Send An Email Using Gmail

        Args:
            from_email (str): Address of the email sender
            email_password (str): Password for the email account of the sender.
              Recommend using an App Password
            to_email (str): Email address for the
            subject (str): Subject of the email
            body (str): Body Contents of the email
        """

        yag = yagmail.SMTP(from_email, email_password)
        yag.send(to=to_email, subject=subject, contents=body, attachments=attachment)
