from util.file_util import read_input_file


class PrintingRules:
    orderings: list[list[int]]
    page_lists: list[list[int]]

    def __init__(self, lines: list[str]):
        self.orderings = []
        self.page_lists = []

        read_orderings = True
        for line in lines:
            if line == "":
                read_orderings = False
            elif read_orderings:
                self.orderings.append(list(map(int, line.split("|"))))
            else:
                self.page_lists.append(list(map(int, line.split(","))))


class PrinterRun:
    orderings: list[list[int]]
    pages: list[int]
    inverse_orderings_per_page: dict[int, list[int]]

    def __init__(self, orderings: list[list[int]], pages: list[int]):
        self.pages = pages
        self.orderings = orderings
        self.inverse_orderings_per_page = self.construct_inverse_orderings(orderings, pages)

    @staticmethod
    def construct_inverse_orderings(orderings: list[list[int]], pages: list[int]) -> dict[int, list[int]]:
        pages = set(pages)
        inverse_orderings_per_page = {}
        for ordering in orderings:
            if ordering[0] in pages and ordering[1] in pages:
                if ordering[1] not in inverse_orderings_per_page:
                    inverse_orderings_per_page[ordering[1]] = []
                inverse_orderings_per_page[ordering[1]].append(ordering[0])
        return inverse_orderings_per_page

    def is_correct(self) -> bool:
        is_printed = set()
        for page in self.pages:
            if page in self.inverse_orderings_per_page:
                for other_pages in self.inverse_orderings_per_page[page]:
                    if other_pages not in is_printed:
                        return False
            is_printed.add(page)
        return True

    def get_ordered_pages(self) -> list[int]:
        ordered_pages = []
        remaining_pages = self.pages.copy()
        inverse_orderings = self.inverse_orderings_per_page
        while remaining_pages:
            new_remaining_pages = []
            for page in remaining_pages:
                if page not in inverse_orderings:
                    ordered_pages.append(page)
                else:
                    new_remaining_pages.append(page)

            if len(new_remaining_pages) == len(remaining_pages):
                raise ValueError("Couldn't find a new page to print!")

            remaining_pages = new_remaining_pages
            inverse_orderings = self.construct_inverse_orderings(self.orderings, new_remaining_pages)
        return ordered_pages


def parse_input_file() -> PrintingRules:
    return PrintingRules(read_input_file(5))


def level5() -> tuple[int, int]:
    printing_rules = parse_input_file()
    sum_middle_numbers_correct = 0
    sum_middle_numbers_incorrect = 0
    for pages in printing_rules.page_lists:
        printer_run = PrinterRun(printing_rules.orderings, pages)
        if printer_run.is_correct():
            sum_middle_numbers_correct += pages[len(pages) // 2]
        else:
            ordered_pages = printer_run.get_ordered_pages()
            sum_middle_numbers_incorrect += ordered_pages[len(ordered_pages) // 2]
    return sum_middle_numbers_correct, sum_middle_numbers_incorrect


if __name__ == '__main__':
    print("Middle page values: " + str(level5()))


def test_level5():
    assert level5() == (143, 123)
