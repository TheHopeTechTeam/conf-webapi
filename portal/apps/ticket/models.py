from auditlog.registry import auditlog
from django.db import models

from model_utils.models import UUIDModel, SoftDeletableModel

from wagtail.search import index


class TicketType(index.Indexed, UUIDModel, SoftDeletableModel):
    """
    Ticket Type model
    """
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.name

    class Meta:
        db_table = "portal_ticket_type"
        verbose_name = "Ticket Type"
        verbose_name_plural = "Ticket Types"
        ordering = ["name"]

class Ticket(index.Indexed, UUIDModel, SoftDeletableModel):
    """
    Ticket model
    """
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    conference = models.ForeignKey('conference.Conference', on_delete=models.CASCADE)
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "portal_ticket"
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        ordering = ["title"]

class TicketRegisterDetail(index.Indexed, UUIDModel, SoftDeletableModel):
    """
    Ticket Register Detail model
    """

    class Identity(models.TextChoices):
        """
        Identity
        """
        SENIOR_PASTOR = "senior_pastor", "主任牧師"
        PASTOR = "pastor", "牧師"
        EVANGELIST = "evangelist", "傳道"
        THEOLOGY_STUDENT = "theology_student", "神學生"
        MINISTRY_LEADER = "ministry_leader", "事工負責人"
        CONGREGANT = "congregant", "會眾"


    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    ticket_number = models.CharField(max_length=128, blank=True, null=True)
    belong_church = models.CharField(max_length=255, blank=True, null=True)
    identity = models.CharField(max_length=16, choices=Identity.choices, blank=True, null=True)
    registered_at = models.DateTimeField(null=True, blank=True)
    unregistered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.account.display_name} - {self.ticket.title}"

    class Meta:
        db_table = "portal_ticket_register_detail"
        verbose_name = "Ticket Register Detail"
        verbose_name_plural = "Ticket Register Details"
        ordering = ["registered_at"]
        unique_together = ("ticket_number", "ticket", "account")


auditlog.register(TicketType)
auditlog.register(Ticket)
auditlog.register(TicketRegisterDetail)
