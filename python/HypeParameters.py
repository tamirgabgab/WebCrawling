URLS = ["https://www.wikipedia.org/",
        "https://www.walla.co.il/",
        "https://www.mako.co.il/tv",
        "https://www.kan.org.il/page.aspx?landingPageId=1039"]

path = 'URLS_to_crawl'
MAX_THREDS = 4
data_regex = '[a-zA-Z0-9-_.]+@[a-zA-Z0-9-_.]+\.[a-z]{2,3}'
data_name = 'Email'
open_html = True
print_results = True
saved_html_name = 'figure1.html'

css = """
    table
    {
    border-collapse: collapse;
    }
    th
    {
    color: #ffffff;
    background-color: #000000;
    }
    td
    {
    background-color: #cccccc;
    }
    table, th, td
    {
    font-family:Arial, Helvetica, sans-serif;
    border: 1px solid black;
    text-align: left;
    }
    """


class crw_Data:
    main_color = "red"
    link_color = "#eb9234"  # orange
    empty_color = "blue"
    data_color = "limegreen"

    edge_urls_color = "black"
    edge_data_color = "#089c2f"                         # green

    main_url_attrs = {"color": main_color}              # color of main url (in knowlage graph)
    urls_attrs = {"color": link_color}                  # color of linked url (in knowlage graph)
    empty_urls_attrs = {"color": empty_color}           # color of empty url (in knowlage graph)
    data_attrs = {"color": data_color}                  # color of email (in knowlage graph)

    edge_urls_attrs = {"color": edge_urls_color}        # color of edge to url (both graphs)
    edge_data_attrs = {"color": edge_data_color}        # color of edge to email (both graphs)

    main_url_attrs_domain = {"color": main_color}       # color of main url (in domain graph)
    urls_attrs_domain = {"color": link_color}           # color of linked (in domain graph)
    empty_urls_attrs_domain = {"color": empty_color}    # color of empty (in domain graph)
    data_attrs_domain = {"color": data_color}           # color of email (in domain graph)

    legends = {'Main url': main_color, 'Normal url': link_color, 'Empty url': empty_color, data_name: data_color}
    legends_domain = {'Main domain': main_color, 'Normal domain': link_color, data_name: data_color}