"""
Workshop forms
"""
import datetime

from dateutil import parser
from django import forms
from wagtail.admin.forms import WagtailAdminModelForm

from portal.apps.language.models import Language, Translation
from portal.apps.workshop.models import Workshop, WorkshopSchedule
from portal.libs.shared import validator


class CustomCharField(forms.CharField):
    """
    Custom CharField
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class WorkshopForm(WagtailAdminModelForm):
    """
    Workshop form
    """
    title = forms.CharField(required=True, label="Title", template_name="form/tw_input.html")
    participants_limit = forms.IntegerField(
        max_value=99999,
        min_value=0,
        required=False,
        label="Participants Limit",
        template_name="form/tw_input.html"
    )
    start_datetime = forms.DateTimeField(
        required=True,
        label="Start Date and Time",
        template_name="form/tw_datetime.html"
    )
    end_datetime = forms.DateTimeField(
        required=True,
        label="End Date and Time",
        template_name="form/tw_datetime.html"
    )

    def __init__(self, *args, **kwargs):
        languages = Language.objects.filter(is_active=True)
        for language in languages:
            field_name = f"description_{str(language.id)}"
            field = forms.CharField(
                label=f"Description in {language.name}",
                widget=forms.Textarea,
                required=False,
                # help_text=f"Description in {language.name}",
                template_name="form/tw_textarea.html",
            )
            self.base_fields[field_name] = field
            self._meta.exclude.append(field_name)
        super().__init__(*args, **kwargs)

    def clean_start_datetime(self):
        """
        Clean start_datetime
        """
        start_datetime = self.cleaned_data.get("start_datetime")
        if not start_datetime:
            raise forms.ValidationError("Start Date and Time is required")
        if start_datetime < datetime.datetime.now(tz=datetime.timezone.utc):
            raise forms.ValidationError("Start Date and Time should be greater than current Date and Time")
        return start_datetime

    def clean_end_datetime(self):
        """
        Clean end_datetime
        """
        if not self.data.get("start_datetime"):
            raise forms.ValidationError("Start Date and Time is required")
        start_datetime = parser.parse(self.data.get("start_datetime"))
        start_datetime = start_datetime.replace(tzinfo=datetime.timezone.utc)
        end_datetime = self.cleaned_data.get("end_datetime")
        if not end_datetime:
            raise forms.ValidationError("End Date and Time is required")
        if end_datetime < start_datetime:
            raise forms.ValidationError("End Date and Time should be greater than Start Date and Time")
        return end_datetime

    def clean(self):
        """
        Clean
        """
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        """
        Save
        """
        instance: Workshop = super().save(commit=commit)
        schedule_instance = WorkshopSchedule.objects.create(
            workshop=instance,
            start_datetime=self.cleaned_data.get("start_datetime"),
            end_datetime=self.cleaned_data.get("end_datetime")
        )
        translation_objs = []
        for field_name in self.fields:
            if "description_" in field_name:
                language_id = field_name.split("_")[-1]
                translated_text = self.cleaned_data.get(field_name)
                if validator.is_empty(translated_text):
                    continue
                translation_objs.append(
                    Translation(
                        language=Language.objects.get(id=language_id),
                        object_id=instance.id,
                        field_name="description",
                        translated_text=translated_text
                    )
                )
        translation_instances = []
        if len(translation_objs) > 0:
            translation_instances = Translation.objects.bulk_create(
                translation_objs,
                update_conflicts=True,
                update_fields=["translated_text"],
                unique_fields=["language", "object_id", "field_name"]
            )
        if commit:
            schedule_instance.save()
            for translation_instance in translation_instances:
                translation_instance.save()
        return instance

    class Meta:
        """Meta"""
        model = Workshop
        fields = [
            "title",
            "conference",
            "location",
            "instructor",
            "participants_limit",
        ]
        exclude = [
            "start_datetime",
            "end_datetime"
        ]