import json
import requests
from bs4 import BeautifulSoup

url = "https://scrape.smartproxy.com/v1/tasks"

payload = {
    "target": "universal",
    "url": "https://www.reddit.com/r/aww/comments/10vm7bw/that_tail_tuck_at_the_end_is_just_so_precious/",
    "headless": "html",
    "parse": "false"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Basic AUTH"
}


def main():

    response = requests.post(url, json=payload, headers=headers)

    json_data = response.text

    parsed_data = json.loads(json_data)

    content = parsed_data['results'][0]['content']

    # Strip scraped content from backslashes

    stripped_content = content.replace('\\', '')

    htmlopen = open("test.html", "w")

    htmlopen.write(stripped_content)

    htmlopen.close()

    soup = BeautifulSoup(stripped_content, "html.parser")

    data = []

    # Select data points

    username = soup.find_all('a', class_='wM6scouPXXsFDSZmZPHRo DjcdNGtVXPcxG0yiFXIoZ _23wugcdiaj44hdfugIAlnX')

    post_timestamp = soup.find_all('span', class_='_2VF2J19pUIMSLJFky-7PEI')

    post_title = soup.find_all('h1', class_='_eYtD2XCVieq6emjKBH3m')

    comment_count = soup.find_all('span', class_='FHCV02u6Cp2zYL0fhQPsO')

    upvote_percentage = soup.find_all('div', class_='t4Hq30BDzTeJ85vREX7_M')

    subreddit_description = soup.find_all('div', class_='_1zPvgKHteTOub9dKkvrOl4')

    subreddit_name = soup.find_all('span', class_='_19bCWnxeTjqzBElWZfIlJb')

    subreddit_date = soup.find_all('span', class_='_1d4NeAxWOiy0JPz7aXRI64')

    subreddit_members = soup.find_all('div', class_='_3b9utyKN3e_kzVZ5ngPqAu')

    subreddit_members_online = soup.find_all('div', class_='_21RLQh5PvUhC6vOKoFeHUP')

    div_tags = soup.find_all('div', class_='_3tw__eCCe7j-epNCKGXUKk')

    post = {
        "Username": username[0].text,
        "PostedAt": post_timestamp[0].text,
        "PostTitle": post_title[0].text,
        "CommentCount": comment_count[0].text,
        "UpvotePercentage": upvote_percentage[0].text,
        "SubredditDescription": subreddit_description[0].text,
        "SubredditName": subreddit_name[0].text,
        "SubredditCreated": subreddit_date[0].text,
        "SubredditMembers": subreddit_members[0].text,
        "SubredditMembersOnline":subreddit_members_online[0].text

    }

    data.append(post)

    # Extract data points

    for div_tag in div_tags:
        author_tags = div_tag.find_all('a', class_='wM6scouPXXsFDSZmZPHRo DjcdNGtVXPcxG0yiFXIoZ _23wugcdiaj44hdfugIAlnX')
        author_text = [author_tag.text for author_tag in author_tags]

        comment_timestamp_tags = div_tag.find_all('a', class_='_3yx4Dn0W3Yunucf5sVJeFU')
        comment_timestamp_text = [comment_timestamp_tag.text for comment_timestamp_tag in comment_timestamp_tags]

        comment_url_tags = div_tag.find_all('a', class_='_3yx4Dn0W3Yunucf5sVJeFU', href=True)
        comment_url_text = [comment_url_tag['href'] for comment_url_tag in comment_url_tags]

        comment_text_tags = div_tag.find_all('p', class_='_1qeIAgB0cPwnLhDF9XSiJM')
        comment_text_text = [comment_text_tag.text for comment_text_tag in comment_text_tags]

        comment_upvotes_tags = div_tag.find_all('div', class_='_1rZYMD_4xY3gRcSS3p8ODO _25IkBM0rRUqWX5ZojEMAFQ _3ChHiOyYyUkpZ_Nm3ZyM2M')
        comment_upvotes_text = [comment_upvotes_tag.text for comment_upvotes_tag in comment_upvotes_tags]

        element = {

            'CommentAuthorName': author_text,
            'CommentDate': comment_timestamp_text,
            'CommentURL': comment_url_text,
            'CommentText': comment_text_text,
            'CommentUpvotes': comment_upvotes_text

        }
        data.append(element)

    # Save data to JSON

    with open('data.json', 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()
