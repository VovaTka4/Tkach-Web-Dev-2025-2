import pytest

def test_start_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Задание к лабораторной работе" in response.get_data(as_text=True)
    
def test_about_page(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert "Об авторе" in response.get_data(as_text=True)

def test_posts_index(client):
    response = client.get("/posts")
    assert response.status_code == 200
    assert "Последние посты" in response.get_data(as_text=True)

def test_posts_index_template(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch(
            "app.get_posts",
            return_value=posts_list,
            autospec=True
        )
        
        _ = client.get('/posts')
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'posts.html'
        assert context['title'] == 'Посты'
        assert len(context['posts']) == len(posts_list)
    
@pytest.mark.parametrize("index", range(5))      
def test_post_index(client, index):
    response = client.get(f"/posts/{index}")
    assert response.status_code == 200
    assert "Пост" in response.get_data(as_text=True)

@pytest.mark.parametrize("index", range(5))
def test_post_page_template(client, captured_templates, mocker, posts_list, index):
    with captured_templates as templates:
        mocker.patch(
            "app.get_posts",
            return_value=posts_list,
            autospec=True
        )
        
        _ = client.get(f'/posts/{index}')        
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'post.html'
        assert context['title'] == posts_list[index]['title']
        assert context['post'] == posts_list[index]
        
@pytest.mark.parametrize("index", range(5))
def test_post_page_date_format(client, posts_list, index):
    
    response = client.get(f"/posts/{index}")

    page_content = response.get_data(as_text = True)
    
    # print("ТУТ КОНТЕНТ>>>>>>>>", page_content)
    
    post_date = posts_list[index]['date'].strftime('%d.%m.%Y')
    
    # print("ТУТ ДАТА ПРОСТО >>>>>>>>>>>", posts_list[index]['date'])
    # print("ТУТ ДАТА В ФОРМЕ >>>>>>>>", post_date)
    
    assert post_date in page_content  
    
@pytest.mark.parametrize("index", range(6, 10))      
def test_post_404_error(client, index):
    response = client.get(f"/posts/{index}")
    assert response.status_code == 404