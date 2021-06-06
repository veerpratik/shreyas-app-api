from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate(result_set, page_no, page_offset=25):
    # Code for pagination
    paginator = Paginator(result_set, page_offset)
    page = int(page_no)
    total_no_of_records = paginator.count
    try:
        result_set = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result_set = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result_set = paginator.page(paginator.num_pages)

    # Total number of pages
    total_pages = paginator.num_pages

    # Add above params into dictionary
    pagination_dict = {
        'total_no_of_pages': total_pages,
        'total_no_of_records': total_no_of_records,
        'page': page_no,
        'offset': page_offset
    }
    return result_set, pagination_dict