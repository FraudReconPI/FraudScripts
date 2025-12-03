def prompt_choice(prompt, options):
    """Prompt user to choose from options by number."""
    print(prompt)
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")
    while True:
        choice = input("Enter number: ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(options):
                return options[idx - 1]
        print("Invalid choice. Please try again.")

def prompt_yes_no(question):
    """Prompt user for yes/no question, return True/False."""
    while True:
        ans = input(f"{question} (y/n): ").strip().lower()
        if ans in ('y', 'yes'):
            return True
        elif ans in ('n', 'no'):
            return False
        print("Please enter y or n.")

def input_if_confirm(question):
    """Ask yes/no question, if yes then input value."""
    if prompt_yes_no(question):
        return input("Enter value: ").strip()
    return ""

def registrar_prompt():
    authority_name = ""
    if prompt_yes_no("Is the issuing authority explicitly named on the certificate?"):
        authority_name = input("Enter the exact name of the issuing authority: ").strip()

    authority_types = [
        "Hospital / Medical facility",
        "Local civil registry office",
        "Regional civil registry office",
        "National civil registry / vital statistics office",
        "Court / judicial office",
        "Religious institution",
        "Unknown"
    ]
    authority_type = prompt_choice("Select the type of issuing authority:", authority_types)

    address = input_if_confirm("Does the certificate list a physical address for the authority?")
    city = input_if_confirm("Does the certificate list a city or town jurisdiction?")
    district = input_if_confirm("Does the certificate list a district, county, or parish jurisdiction?")
    region = input_if_confirm("Does the certificate list a region, province, or state jurisdiction?")
    country = input_if_confirm("Does the certificate list a country?")
    registrar_name = input_if_confirm("Is the registrar's name listed on the certificate?")
    registration_number = input_if_confirm("Does the certificate include a registration number?")
    file_code = input_if_confirm("Does the certificate include a file or folio code?")
    issue_date = input_if_confirm("Does the certificate list an issue or issuance date?")
    seal_number = input_if_confirm("Does the certificate have any seal, stamp, or office number?")

    signature_type = ""
    if prompt_yes_no("Is there a signature on the certificate?"):
        signature_options = [
            "Registrar signature",
            "Doctor signature",
            "Administrator signature",
            "Illegible / printed / digital"
        ]
        signature_type = prompt_choice("Select the signature type:", signature_options)

    foreign_language_text = input_if_confirm("Is the certificate bilingual or in a foreign language?")

    # Build the prompt text
    lines = []
    if authority_name:
        lines.append(f"Issuing authority: {authority_name}")
    if authority_type:
        lines.append(f"Authority type: {authority_type}")
    if address:
        lines.append(f"Address: {address}")
    if city:
        lines.append(f"City/Town: {city}")
    if district:
        lines.append(f"District/County/Parish: {district}")
    if region:
        lines.append(f"Region/Province/State: {region}")
    if country:
        lines.append(f"Country: {country}")
    if registrar_name:
        lines.append(f"Registrar name: {registrar_name}")
    if registration_number:
        lines.append(f"Registration number: {registration_number}")
    if file_code:
        lines.append(f"File or folio code: {file_code}")
    if issue_date:
        lines.append(f"Issue date: {issue_date}")
    if seal_number:
        lines.append(f"Seal or stamp number: {seal_number}")
    if signature_type:
        lines.append(f"Signature type: {signature_type}")
    if foreign_language_text:
        lines.append(f"Foreign language text / notes: {foreign_language_text}")

    if lines:
        prompt_text = ("Find the contact information (phone and email) for the authority that issued this death certificate.\n\n"
                       + "\n".join(lines)
                       + "\n\nWe need to confirm the certificate was issued and is valid.")
    else:
        prompt_text = "No details were entered."

    print("\n=== Generated Prompt ===\n")
    print(prompt_text)
    print("\n========================\n")

def generic_facility_prompt(facility_type):
    address = ""
    city = ""
    name = ""

    if prompt_yes_no(f"Do you have a full address for the {facility_type}?"):
        address = input(f"Enter the full address of the {facility_type}: ").strip()
    else:
        city = input(f"Enter the city for the {facility_type}: ").strip()

    if prompt_yes_no(f"Do you have the name of the {facility_type}?"):
        name = input(f"Enter the name of the {facility_type}: ").strip()

    lines = []
    country = input_if_confirm("Do you want to specify the country? If yes, enter it now.")
    if name and address:
        lines.append(f"We need contact information for {name} at {address} (phone and email). This is in {country if country else '[Country unspecified]'}")
    elif name and city:
        lines.append(f"We need the contact information and full address for {name} in {city} (phone and email). This is in {country if country else '[Country unspecified]'}")
    elif address:
        lines.append(f"We need the contact information for the {facility_type} located at {address} (phone and email). This is in {country if country else '[Country unspecified]'}")
    else:
        lines.append(f"We need the contact information for the {facility_type} in {city if city else '[City unspecified]'} (phone and email). This is in {country if country else '[Country unspecified]'}")

    print("\n=== Generated Prompt ===\n")
    print("\n".join(lines))
    print("\n========================\n")

def doctor_prompt():
    doctor_name = input("Enter the doctor's name: ").strip()
    city = input("Enter the city: ").strip()
    facility_name = ""
    if prompt_yes_no("Do we know the name of the medical facility?"):
        facility_name = input("Enter the medical facility name: ").strip()

    country = input_if_confirm("Do you want to specify the country?")

    lines = []
    if doctor_name and facility_name:
        lines.append(f"We need contact information for doctor {doctor_name} at {facility_name} in {city} in {country if country else '[Country unspecified]'} (phone and email).")
    elif doctor_name and city:
        lines.append(f"We need the contact information and full address for {doctor_name} in {city} in {country if country else '[Country unspecified]'} (phone and email).")
    else:
        lines.append("Insufficient details to generate prompt.")

    print("\n=== Generated Prompt ===\n")
    print("\n".join(lines))
    print("\n========================\n")

def main():
    print("Select facility type to create prompt for:")
    facility_types = [
        "Registrar",
        "Hospital",
        "Doctor",
        "Mortuary",
        "Crematory",
        "Cemetery"
    ]

    choice = prompt_choice("Facility types:", facility_types)

    if choice == "Registrar":
        registrar_prompt()
    elif choice == "Hospital":
        generic_facility_prompt("hospital")
    elif choice == "Doctor":
        doctor_prompt()
    elif choice == "Mortuary":
        generic_facility_prompt("mortuary")
    elif choice == "Crematory":
        generic_facility_prompt("crematory")
    elif choice == "Cemetery":
        generic_facility_prompt("cemetery")

if __name__ == "__main__":
    main()
