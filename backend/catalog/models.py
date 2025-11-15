"""Test catalog models."""

from django.db import models


class TestCatalog(models.Model):
    """Test catalog model for available lab tests."""

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100)
    sample_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    turnaround_time_hours = models.IntegerField(help_text="Expected TAT in hours")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "test_catalog"
        ordering = ["code"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["category"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Parameter(models.Model):
    """Parameter (Analyte) model - maps to Excel 'Parameters' sheet."""

    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=50, blank=True)
    data_type = models.CharField(max_length=50, default="Numeric")
    editor_type = models.CharField(max_length=50, default="Plain")
    decimal_places = models.IntegerField(default=2, null=True, blank=True)
    allowed_values = models.TextField(blank=True)
    is_calculated = models.BooleanField(default=False)
    calculation_formula = models.TextField(blank=True)
    flag_direction = models.CharField(max_length=20, default="Both")
    has_quick_text = models.BooleanField(default=False)
    external_code_type = models.CharField(max_length=50, blank=True)
    external_code_value = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "parameters"
        ordering = ["code"]
        indexes = [
            models.Index(fields=["code"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Test(models.Model):
    """Test model - maps to Excel 'Tests' sheet."""

    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=100, blank=True)
    test_type = models.CharField(max_length=50, default="Single")
    department = models.CharField(max_length=100, blank=True)
    specimen_type = models.CharField(max_length=100, blank=True)
    container_type = models.CharField(max_length=100, blank=True)
    result_scale = models.CharField(max_length=50, blank=True)
    default_method = models.CharField(max_length=100, blank=True)
    default_tat_minutes = models.IntegerField(default=0)
    default_print_group = models.CharField(max_length=100, blank=True)
    default_report_template = models.CharField(max_length=100, blank=True)
    default_printer_code = models.CharField(max_length=50, blank=True)
    billing_code = models.CharField(max_length=50, blank=True)
    default_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    external_code_type = models.CharField(max_length=50, blank=True)
    external_code_value = models.CharField(max_length=100, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tests"
        ordering = ["code"]
        indexes = [
            models.Index(fields=["code"]),
            models.Index(fields=["department"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class TestParameter(models.Model):
    """Test-Parameter relationship model - maps to Excel 'Test_Parameters' sheet."""

    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="test_parameters")
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name="test_parameters")
    display_order = models.IntegerField(default=0)
    section_header = models.CharField(max_length=255, blank=True)
    is_mandatory = models.BooleanField(default=True)
    show_on_report = models.BooleanField(default=True)
    default_reference_profile_id = models.CharField(max_length=50, blank=True)
    delta_check_enabled = models.BooleanField(default=False)
    panic_low_override = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    panic_high_override = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    comment_template_id = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "test_parameters"
        unique_together = [["test", "parameter"]]
        ordering = ["test", "display_order"]
        indexes = [
            models.Index(fields=["test", "display_order"]),
        ]

    def __str__(self):
        return f"{self.test.code} - {self.parameter.code}"


class ReferenceRange(models.Model):
    """Reference range model - maps to Excel 'Reference_Ranges' sheet."""

    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name="reference_ranges")
    method_code = models.CharField(max_length=50, blank=True)
    sex = models.CharField(max_length=20, default="All")
    age_min = models.IntegerField(default=0)
    age_max = models.IntegerField(default=999)
    age_unit = models.CharField(max_length=20, default="Years")
    population_group = models.CharField(max_length=50, default="Adult")
    unit = models.CharField(max_length=50, blank=True)
    normal_low = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    normal_high = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    critical_low = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    critical_high = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reference_text = models.TextField(blank=True)
    effective_from = models.DateField(null=True, blank=True)
    effective_to = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reference_ranges"
        ordering = ["parameter", "age_min"]
        indexes = [
            models.Index(fields=["parameter", "sex", "age_min"]),
        ]

    def __str__(self):
        return f"{self.parameter.code} - {self.sex} ({self.age_min}-{self.age_max} {self.age_unit})"


class ParameterQuickText(models.Model):
    """Parameter quick text templates model - maps to Excel 'Parameter_Quick_Text' sheet."""

    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name="quick_texts")
    template_title = models.CharField(max_length=255)
    template_body = models.TextField()
    language = models.CharField(max_length=10, default="EN")
    is_default = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "parameter_quick_texts"
        unique_together = [["parameter", "template_title", "language"]]
        ordering = ["parameter", "template_title"]
        indexes = [
            models.Index(fields=["parameter"]),
        ]

    def __str__(self):
        return f"{self.parameter.code} - {self.template_title}"
