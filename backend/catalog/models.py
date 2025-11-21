"""Test catalog models."""

from django.db import models


class TestCatalog(models.Model):
    """
    Represents an available lab test in the catalog.

    This model stores the details of each test that can be ordered, including
    its code, name, price, and other metadata. It serves as the master list of
    all available tests.

    Attributes:
        code (str): A unique code for the test.
        name (str): The full name of the test.
        description (str): A detailed description of the test.
        category (str): The category the test belongs to (e.g., 'Hematology').
        sample_type (str): The type of sample required (e.g., 'Blood').
        price (Decimal): The price of the test.
        turnaround_time_hours (int): The expected turnaround time in hours.
        is_active (bool): Whether the test is currently available.
    """

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
    """
    Represents a single parameter or analyte that can be measured.

    This model defines the individual components of a test, such as 'Hemoglobin'
    or 'Glucose'. It includes details about the parameter's units, data type,
    and how it should be displayed.

    Attributes:
        code (str): A unique code for the parameter.
        name (str): The full name of the parameter.
        unit (str): The unit of measurement (e.g., 'g/dL', 'mg/dL').
        data_type (str): The type of data (e.g., 'Numeric', 'Text').
        is_calculated (bool): Whether the parameter is calculated from others.
    """

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
    """
    Represents a single orderable test, which may consist of multiple parameters.

    This model is a more detailed representation of a test than `TestCatalog`,
    and it is used for linking tests to their constituent parameters. It is
    imported from the 'Tests' sheet of the LIMS master Excel file.

    Attributes:
        code (str): A unique code for the test.
        name (str): The full name of the test.
        department (str): The lab department that performs the test.
        specimen_type (str): The type of specimen required.
        default_charge (Decimal): The default price for the test.
    """

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
    """
    Links a `Test` to its constituent `Parameter` models.

    This model creates a many-to-many relationship between tests and parameters,
    defining which parameters are included in each test. It also specifies the
    order in which the parameters should be displayed.

    Attributes:
        test (Test): The test that includes the parameter.
        parameter (Parameter): The parameter included in the test.
        display_order (int): The order of the parameter within the test.
    """

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
    """
    Defines the normal reference ranges for a `Parameter`.

    This model stores the low and high values of a parameter that are considered
    normal, as well as critical thresholds. The ranges can be specific to
    demographics such as age and sex.

    Attributes:
        parameter (Parameter): The parameter these ranges apply to.
        sex (str): The sex the range applies to ('Male', 'Female', 'All').
        age_min (int): The minimum age for this range.
        age_max (int): The maximum age for this range.
        normal_low (Decimal): The lower bound of the normal range.
        normal_high (Decimal): The upper bound of the normal range.
    """

    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name="reference_ranges")
    method_code = models.CharField(max_length=50, blank=True)
    sex = models.CharField(max_length=20, default="All")
    age_min = models.IntegerField(default=0)
    age_max = models.IntegerField(default=999)
    age_unit = models.CharField(max_length=20, default="Years")
    population_group = models.CharField(max_length=50, default="Adult")
    unit = models.CharField(max_length=50, blank=True)
    normal_low = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    normal_high = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    critical_low = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    critical_high = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
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
    """
    Stores predefined text templates for `Parameter` results.

    This model allows for the creation of quick text snippets that can be easily
    inserted into parameter results, saving time for technologists. For example,
    a 'remarks' parameter might have quick text options like 'Sample was hemolyzed'.

    Attributes:
        parameter (Parameter): The parameter the quick text applies to.
        template_title (str): A short title for the template.
        template_body (str): The full text of the template.
    """

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
