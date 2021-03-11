
def get_list_of_recent_searches(cursor, recent_text_search, user_id, channel_id):

    get_recent_searches_sql = '''
        select searches.search_text
        from search_history
        inner join searches on search_history.search_id = searches.id
        inner join member on search_history.member_id = member.id
        where
        searches.search_text LIKE '%{recent_text_search}%' and
        member.channel_id = '{channel_id}' and
        member.user_id = '{user_id}';
    '''.format(
        recent_text_search=recent_text_search,
        channel_id=channel_id,
        user_id=user_id
    )
    cursor.execute(get_recent_searches_sql)
    result = cursor.fetchall()

    return result
