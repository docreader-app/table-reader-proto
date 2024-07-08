from google.api_core.client_options import ClientOptions
from google.api_core.exceptions import NotFound
from google.cloud import documentai  # type: ignore
from google.cloud.documentai_toolbox import document

# TODO(developer): Uncomment these variables before running the sample.
project_id = 'windy-energy-427505-m8'
location = 'us' # Format is 'us' or 'eu'
processor_display_name = 'docreader-test-ocr' # Must be unique per project, e.g.: 'My Processor'
processor_type = 'FORM_PARSER_PROCESSOR' # Use fetch_processor_types to get available processor types

def fetch_processor_types_sample(project_id: str, location: str) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location
    # e.g.: projects/project_id/locations/location
    parent = client.common_location_path(project_id, location)

    # Fetch all processor types
    response = client.fetch_processor_types(parent=parent)

    print("Processor types:")
    # Print the available processor types
    for processor_type in response.processor_types:
        if processor_type.allow_creation:
            print(processor_type.type_)


def create_processor_sample(project_id: str, location: str, processor_display_name: str, processor_type: str) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location
    # e.g.: projects/project_id/locations/location
    parent = client.common_location_path(project_id, location)

    # Create a processor
    processor = client.create_processor(
        parent=parent,
        processor=documentai.Processor(
            display_name=processor_display_name, type_=processor_type
        ),
    )

    # Print the processor information
    print(f"Processor Name: {processor.name}")
    print(f"Processor Display Name: {processor.display_name}")
    print(f"Processor Type: {processor.type_}")



def list_processors_sample(project_id: str, location: str) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location
    # e.g.: projects/project_id/locations/location
    parent = client.common_location_path(project_id, location)

    # Make ListProcessors request
    processor_list = client.list_processors(parent=parent)

    # Print the processor information
    for processor in processor_list:
        print(f"Processor Name: {processor.name}")
        print(f"Processor Display Name: {processor.display_name}")
        print(f"Processor Type: {processor.type_}")
        print("")


def delete_processor_sample(project_id: str, location: str, processor_id: str) -> None:
    # You must set the api_endpoint if you use a location other than 'us'.
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor
    # e.g.: projects/project_id/locations/location/processors/processor_id
    processor_name = client.processor_path(project_id, location, processor_id)

    # Delete a processor
    try:
        operation = client.delete_processor(name=processor_name)
        # Print operation details
        print(operation.operation.name)
        # Wait for operation to complete
        operation.result()
    except NotFound as e:
        print(e.message)


def table_sample(documentai_doc, output_file_prefix: str) -> None:
    wrapped_document = document.Document.from_documentai_document(documentai_document=documentai_doc)

    print("Tables in Document")
    for page in wrapped_document.pages:
        for table_index, table in enumerate(page.tables):
            # Convert table to Pandas Dataframe
            # Refer to https://pandas.pydata.org/docs/reference/frame.html for all supported methods
            df = table.to_dataframe()
            print(df)

            output_filename = f"{output_file_prefix}-{page.page_number}-{table_index}"

            # Write Dataframe to CSV file
            df.to_csv(f"{output_filename}.csv", index=False)

            # # Write Dataframe to HTML file
            # df.to_html(f"{output_filename}.html", index=False)

            # # Write Dataframe to Markdown file
            # df.to_markdown(f"{output_filename}.md", index=False)


def quickstart(
    project_id: str,
    location: str,
    file_path: str,
    processor_display_name: str = "docreader-ocr",
):
    # You must set the `api_endpoint`if you use a location other than "us".
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the location, e.g.:
    # `projects/{project_id}/locations/{location}`
    parent = client.common_location_path(project_id, location)

    processor_list = client.list_processors(parent=parent)
    proc_found = False
    # Create a Processor
    for proc in processor_list:
        if proc.display_name == processor_display_name:
            processor = proc
            proc_found = True

    if not proc_found:
        processor = client.create_processor(
            parent=parent,
            processor=documentai.Processor(
                type_="FORM_PARSER_PROCESSOR",  # Refer to https://cloud.google.com/document-ai/docs/create-processor for how to get available processor types
                display_name=processor_display_name,
            ),
        )

    # Print the processor information
    print(f"Processor Name: {processor.name}")

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Load binary data
    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type="application/pdf",  # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
    )

    # Configure the process request
    # `processor.name` is the full resource name of the processor, e.g.:
    # `projects/{project_id}/locations/{location}/processors/{processor_id}`
    request = documentai.ProcessRequest(name=processor.name, raw_document=raw_document)

    result = client.process_document(request=request)

    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    document = result.document

    # Read the text recognition output from the processor
    print("The document contains the following text:")
    print(document.text)

    output_file_prefix = 'csvtest'

    table_sample(documentai_doc=document, output_file_prefix=output_file_prefix)

   


# fetch_processor_types_sample(project_id=project_id, location=location)

# create_processor_sample(project_id=project_id, location=location, processor_display_name=processor_display_name, processor_type=processor_type)

list_processors_sample(project_id=project_id, location=location)

quickstart(project_id=project_id, location=location, file_path='CBP_Manual_1948_part1-pages.pdf', processor_display_name='docreader-form')