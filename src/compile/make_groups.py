

def get_sub_only(row, sub_col, dub_col):
    try:
        result = bool(row[sub_col] and not row[dub_col])
    except KeyError:
        try:
            result = bool(row[sub_col])
        except KeyError:
            result = False

    return result


def get_dub_only(row, sub_col, dub_col):
    try:
        result = bool(row[dub_col] and not row[sub_col])
    except KeyError:
        try:
            result = bool(row[dub_col])
        except KeyError:
            result = False

    return result


def get_sub_and_dub(row, sub_col, dub_col):
    try:
        result = bool(row[dub_col] and row[sub_col])
    except KeyError:
        result = False
    return result


def get_neither(row, sub_col, dub_col):
    try:
        result = bool(row[dub_col] and row[sub_col])
    except KeyError:
        try:
            result = bool(row[dub_col])
        except KeyError:
            try:
                result = bool(row[sub_col])
            except KeyError:
                result = False

    return result


def set_exclusive_columns(row, language):
    sub_col = f'sub_{language}'
    dub_col = f'dub_{language}'

    row[f'grp_neither_{language}'] = get_neither(row, sub_col, dub_col)
    row[f'grp_sub_only_{language}'] = get_sub_only(row, sub_col, dub_col)
    row[f'grp_dub_only_{language}'] = get_dub_only(row, sub_col, dub_col)
    row[f'grp_both_{language}'] = get_sub_and_dub(row, sub_col, dub_col)

    return row


def get_all_languages(df):
    sub_list = [item.split('_')[1] for item in df.columns if item.startswith('sub')]
    dub_list = [item.split('_')[1] for item in df.columns if item.startswith('dub')]

    lang_list = list(set(sub_list + dub_list))
    return lang_list


def perform_make_exclusive(df):
    lang_list = get_all_languages(df)
    max_count = len(lang_list)
    count = 1
    for lang in lang_list:
        print(f'({count}/{max_count})Grouping {lang}')
        df = df.apply(lambda x: set_exclusive_columns(x, language=lang), axis=1)
        count += 1

    new_df = df[[item for item in df.columns if not item[:3] in ['sub', 'dub']]]
    return new_df