from pydur import students, get_random_pairs


def main():
    print('\n'.join([' & '.join(pair) for pair in get_random_pairs(students)]))


if __name__ == '__main__':
    main()
