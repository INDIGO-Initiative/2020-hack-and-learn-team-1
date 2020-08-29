import requests
import csv
import jsonpointer

BASE_URL = "https://golab-indigo-data-store.herokuapp.com"


# From https://github.com/INDIGO-Initiative/database-app/blob/live/indigo/__init__.py
# Then "relation" xey added my hand
TYPE_PROJECT_ORGANISATION_REFERENCES_LIST = [
    {
        "list_key": "/service_provisions",
        "item_organisation_id_key": "/organisation_id/value",
        "relation": "Service Provision",
    },
    {
        "list_key": "/outcome_payment_commitments",
        "item_organisation_id_key": "/organisation_id/value",
        "relation": "Outcome Payment Commitments",
    },
    {"list_key": "/investments", "item_organisation_id_key": "/organisation_id/value",
        "relation": "Investments",},
    {
        "list_key": "/intermediary_services",
        "item_organisation_id_key": "/organisation_id/value",
        "relation": "Intermediary Services",
    },
    {
        "list_key": "/transactions",
        "item_organisation_id_key": "/sending_organisation_id/value",
        "relation": "Transaction (Sending)",
    },
    {
        "list_key": "/transactions",
        "item_organisation_id_key": "/receiving_organisation_id/value",
        "relation": "Transaction (Receiving)",
    },
    {
        "list_key": "/grants",
        "item_organisation_id_key": "/recipient_organisation_id/value",
        "relation": "Grant (Recipient)",
    },
    {
        "list_key": "/grants",
        "item_organisation_id_key": "/funding_organisation_id/value",
        "relation": "Grant (Funding)",
    },
    {
        "list_key": "/technical_assistances",
        "item_organisation_id_key": "/recipient_organisation_id/value",
        "relation": "Technical Assistance (Recipient)",
    },
    {
        "list_key": "/technical_assistances",
        "item_organisation_id_key": "/funding_organisation_id/value",
        "relation": "Technical Assistance (Funding)",
    },
]

def go():
    r1 = requests.get(BASE_URL + '/app/api1/project')


    with open('out.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([
            "Project: ID",
            "Relationship",
            "Organisation: ID",
        ])

        project_ids = [d.get('id') for d in r1.json().get('projects') if d.get('public')]
        project_ids.sort()

        for project_id in project_ids:
                print(project_id)
                request_project =  requests.get(BASE_URL + '/app/api1/project/' + project_id)
                project_data = request_project.json()

                for spec in TYPE_PROJECT_ORGANISATION_REFERENCES_LIST:

                    data_list = jsonpointer.resolve_pointer(project_data, "/project/data" + spec['list_key'], [])
                    for data_item in data_list:

                        org_id = jsonpointer.resolve_pointer(data_item, spec['item_organisation_id_key'], [])
                        if org_id:
                            row = [
                                project_id,
                                spec['relation'],
                                org_id,
                            ]

                            writer.writerow(row)


if __name__ == "__main__":
    go()
