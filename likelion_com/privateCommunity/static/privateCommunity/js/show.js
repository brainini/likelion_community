
const onClickDeleteButtonDetail = async (postId) => {
    if (confirm("정말 삭제하시겠습니까?")) {
      // 확인 버튼 클릭 시 동작
      response = await axios.delete(`/community/posts/${postId}/delete/`);
      window.location.href = 'http://127.0.0.1:8000/community/'
    }
    else;
}



const getCommentElement = (content, postId, commentId, author, created_at) => {
	
    let newCommentDiv = document.createElement('div');
    newCommentDiv.setAttribute('id',`${commentId}-comment`);
    newCommentDiv.setAttribute('class', 'comment-box');
    let newCommentElement = document.createElement('div');
    let newCommentContent = document.createElement('p');
    newCommentContent.innerHTML = `${author}: ${content} &nbsp; &nbsp;${created_at} &nbsp;`;
    newCommentElement.appendChild(newCommentContent);
    newCommentDiv.appendChild(newCommentElement);


    let replyButton = document.createElement('button');
    replyButton.setAttribute('onclick', `makeRecommentBox(${postId},${commentId})`);
    replyButton.setAttribute('class', `make-recomment-button`);
    replyButton.innerHTML = "대댓글 달기";
    newCommentDiv.appendChild(replyButton);

    let likeboxParent = document.createElement('button');
    likeboxParent.innerHTML = '좋아요';
    likeboxParent.setAttribute('class', 'like-box-parent');

    let likeboxChild = document.createElement('div');
    likeboxChild.setAttribute('class', 'like-box-child');

    let bestdiv = document.createElement('div');
    bestdiv.setAttribute('class', 'emotion-best');
    let bestlink = document.createElement('a');
    bestlink.setAttribute('id', `${commentId}-comment-best-button`);
    bestlink.setAttribute('onclick', `onClickCommentBestButton(${postId}, ${commentId})`);
    bestimg = document.createElement('img');
    bestimg.setAttribute('class', 'emotion');
    bestimg.setAttribute('src', "/static/privateCommunity/img/best.png");
    bestlink.appendChild(bestimg);
    bestdiv.appendChild(bestlink);
    likeboxChild.appendChild(bestdiv);

    let thanksdiv = document.createElement('div');
    thanksdiv.setAttribute('class', 'emotion-thanks');
    let thankslink = document.createElement('a');
    thankslink.setAttribute('id', `${commentId}-comment-thanks-button`);
    thankslink.setAttribute('onclick', `onClickCommentThanksButton(${postId}, ${commentId})`);
    thanksimg = document.createElement('img');
    thanksimg.setAttribute('class', 'emotion');
    thanksimg.setAttribute('src', "/static/privateCommunity/img/thanks.png");
    thankslink.appendChild(thanksimg);
    thanksdiv.appendChild(thankslink);
    likeboxChild.appendChild(thanksdiv);

    let surprisingdiv = document.createElement('div');
    surprisingdiv.setAttribute('class', 'emotion-surprising');
    let surprisinglink = document.createElement('a');
    surprisinglink.setAttribute('id', `${commentId}-comment-surprising-button`);
    surprisinglink.setAttribute('onclick', `onClickCommentSurprisingButton(${postId}, ${commentId})`);
    surprisingimg = document.createElement('img');
    surprisingimg.setAttribute('class', 'emotion');
    surprisingimg.setAttribute('src', "/static/privateCommunity/img/surprising.png");
    surprisinglink.appendChild(surprisingimg);
    surprisingdiv.appendChild(surprisinglink);
    likeboxChild.appendChild(surprisingdiv);

    let funnydiv = document.createElement('div');
    funnydiv.setAttribute('class', 'emotion-funny');
    let funnylink = document.createElement('a');
    funnylink.setAttribute('id', `${commentId}-comment-funny-button`);
    funnylink.setAttribute('onclick', `onClickCommentFunnyButton(${postId}, ${commentId})`);
    funnyimg = document.createElement('img');
    funnyimg.setAttribute('class', 'emotion');
    funnyimg.setAttribute('src', "/static/privateCommunity/img/funny.png");
    funnylink.appendChild(funnyimg);
    funnydiv.appendChild(funnylink);
    likeboxChild.appendChild(funnydiv);

    likeboxParent.appendChild(likeboxChild);
    newCommentDiv.appendChild(likeboxParent);

    let deleteDiv = document.createElement('div');
    let deleteButton = document.createElement('a');
    deleteButton.setAttribute('onclick', `onClickCommentDelete(${postId},${commentId})`);
    deleteButton.innerHTML = "&nbsp;&nbsp;삭제";
    deleteDiv.appendChild(deleteButton);
    newCommentDiv.appendChild(deleteDiv);
  
  
    recomment_list = document.createElement('div');
    recomment_list.setAttribute('id', `${commentId}-recomment-list`);
    recomment_list.setAttribute('class', 'recomment-list');
    recomment_list.appendChild(document.createElement('div'));
    newCommentDiv.appendChild(recomment_list);
    
    return newCommentDiv; 
}
  
const onAddComment = async (postId) => {
    const commentInputElement = document.getElementById("comment-input");
    if(commentInputElement.value) {
        // axios로 보내줄 data Form을 만들어 줍니다. 
        let data = new FormData();
        // content라는 key를 만들고, tag input 값을 적어줍니다. 
        data.append("content", commentInputElement.value);
        // aixos 요청에 의한 응답을 받을 때까지 기다렷다가 response에 할당해준다. 
        const response = await axios.post(`/community/posts/${postId}/comments/`, data);
        const commentElement = getCommentElement(commentInputElement.value, postId, response.data.commentId, response.data.author, response.data.created_at);
        document.getElementById("comment-list").appendChild(commentElement);

        commentInputElement.value="";
        const commentCount = document.getElementById('comment-count');
        commentCount.innerHTML = `<strong>댓글이 ${response.data.commentCount}개 있습니다</strong>`;
    }
}

const getReCommentElement = (content, postId, recommentId, author, created_at) => {
	
    let newReCommentElement = document.createElement('p');
    newReCommentElement.setAttribute('id',`${recommentId}-recomment`);
    newReCommentElement.innerHTML = `&nbsp; &nbsp;&nbsp; &nbsp; ㄴ> ${author}: ${content} &nbsp; &nbsp;${created_at} &nbsp;`;
    
    // let likeButton = document.createElement('a');
    // likeButton.setAttribute('onclick', `onClickCommentLike(${postId},${commentId})`);
    // likeButton.setAttribute('id', `${commentId}-comment-like-button`);
    // likeButton.innerHTML = "0 Likes";
    // let deleteButton = document.createElement('a');
    // deleteButton.setAttribute('onclick', `onClickCommentDelete(${postId},${commentId})`);
    // deleteButton.innerHTML = " 댓글 삭제"
  
    // newReCommentElement.appendChild(likeButton);
    // newReCommentElement.appendChild(deleteButton);
    
    return newReCommentElement; 
}
  
const onAddReComment = async (postId, commentId) => {
    const recommentInputElement = document.getElementById(`${commentId}-recomment-input`);
    if(recommentInputElement.value) {
        // axios로 보내줄 data Form을 만들어 줍니다. 
        let data = new FormData();
        // content라는 key를 만들고, tag input 값을 적어줍니다. 
        data.append("content", recommentInputElement.value);
            // aixos 요청에 의한 응답을 받을 때까지 기다렷다가 response에 할당해준다. 
        const response = await axios.post(`/community/posts/${postId}/comments/${commentId}/`, data);

        // delete existing recomment input box
        const recomment_list = document.getElementById(`${commentId}-recomment-list`);
        recomment_list.lastChild.remove();
        recomment_list.lastChild.remove();
        recomment_list.lastChild.remove();

        const recommentElement = getReCommentElement(recommentInputElement.value, postId, response.data.recommentId, response.data.author, response.data.created_at);
        recomment_list.appendChild(recommentElement);
        const commentCount = document.getElementById('comment-count');
        commentCount.innerHTML = `<strong>댓글이 ${response.data.commentCount}개 있습니다</strong>`;
    }
}

const onClickCommentDelete = async (postId, commentId) => {
    if (confirm("정말 삭제하시겠습니까?")) {
      // 확인 버튼 클릭 시 동작
      const deletedComment = document.getElementById(`${commentId}-comment`);
      deletedComment.style.display = 'none';
      response = await axios.delete(`/community/posts/${postId}/comments/${commentId}/delete`);
      const commentCount = document.getElementById('comment-count');
      commentCount.innerHTML = `<strong>댓글이 ${response.data.commentCount}개 있습니다</strong>`;
    }
    else;
}

const onClickReCommentDelete = async (postId, commentId, recommentId) => {
    if (confirm("정말 삭제하시겠습니까?")) {
      // 확인 버튼 클릭 시 동작
      const deletedComment = document.getElementById(`${recommentId}-recomment`);
      deletedComment.style.display = 'none';
      response = await axios.delete(`/posts/${postId}/comments/${commentId}/delete/${recommentId}`);
      const commentCount = document.getElementById('comment-count');
      commentCount.innerHTML = `<strong>댓글이 ${response.data.commentCount}개 있습니다</strong>`;
    }
    else;
}
/// 비동기 게시글 감정표현
const onClickPostBestButton = async (postId) => {
    const post_best_button = document.getElementById("post-best-button")
    const response = await axios.post(`/community/posts/${postId}/emotion/best/`)
    post_best_button.firstElementChild.innerHTML = `${response.data.postBestCount}`
}

const onClickPostThanksButton = async (postId) => {
    const post_thanks_button = document.getElementById("post-thanks-button")
    const response = await axios.post(`/community/posts/${postId}/emotion/thanks/`)
    post_thanks_button.firstElementChild.innerHTML = `${response.data.postThanksCount}`
}

const onClickPostSurprisingButton = async (postId) => {
    const post_surprising_button = document.getElementById("post-surprising-button")
    const response = await axios.post(`/community/posts/${postId}/emotion/surprising/`)
    post_surprising_button.firstElementChild.innerHTML = `${response.data.postSurprisingCount}`
}

const onClickPostFunnyButton = async (postId) => {
    const post_funny_button = document.getElementById("post-funny-button")
    const response = await axios.post(`/community/posts/${postId}/emotion/funny/`)
    post_funny_button.firstElementChild.innerHTML = `${response.data.postFunnyCount}`
}

/// 비동기 댓글 감정표현
const onClickCommentBestButton = async (postId, commentId) => {
    const comment_best_button = document.getElementById(`${commentId}-comment-best-button`)
    const response = await axios.post(`/community/posts/${postId}/comments/${commentId}/commentEmotion/best/`)
    comment_best_button.firstElementChild.innerHTML = `${response.data.bestCount}`
}

const onClickCommentThanksButton = async (postId, commentId) => {
    const comment_thanks_button = document.getElementById(`${commentId}-comment-thanks-button`)
    const response = await axios.post(`/community/posts/${postId}/comments/${commentId}/commentEmotion/thanks/`)
    comment_thanks_button.firstElementChild.innerHTML = `${response.data.thanksCount}`
}

const onClickCommentSurprisingButton = async (postId, commentId) => {
    const comment_surprising_button = document.getElementById(`${commentId}-comment-surprising-button`)
    const response = await axios.post(`/community/posts/${postId}/comments/${commentId}/commentEmotion/surprising/`)
    comment_surprising_button.firstElementChild.innerHTML = `${response.data.surprisingCount}`
}

const onClickCommentFunnyButton = async (postId, commentId) => {
    const comment_funny_button = document.getElementById(`${commentId}-comment-funny-button`)
    const response = await axios.post(`/community/posts/${postId}/comments/${commentId}/commentEmotion/funny/`)
    comment_funny_button.firstElementChild.innerHTML = `${response.data.funnyCount}`
}


/// 비동기 대댓글 감정표현
const onClickReCommentBestButton = async (postId, commentId, recommentId) => {
    const recomment_best_button = document.getElementById(`${recommentId}-recomment-best-button`)
    const response = await axios.post(`/community/posts/${postId}/comments/${commentId}/recomments/${recommentId}/recommentEmotion/best/`)
    recomment_best_button.firstElementChild.innerHTML = `${response.data.bestCount}`
}

const onClickReCommentThanksButton = async (postId, commentId, recommentId) => {
    const recomment_thanks_button = document.getElementById(`${recommentId}-recomment-thanks-button`)
    const response = await axios.post(`/community/posts/${postId}/comments/${commentId}/recomments/${recommentId}/recommentEmotion/thanks/`)
    recomment_thanks_button.firstElementChild.innerHTML = `${response.data.thanksCount}`
}

const onClickReCommentSurprisingButton = async (postId, commentId, recommentId) => {
    const recomment_surprising_button = document.getElementById(`${recommentId}-recomment-surprising-button`)
    const response = await axios.post(`/community/posts/${postId}/comments/${commentId}/recomments/${recommentId}/recommentEmotion/surprising/`)
    recomment_surprising_button.firstElementChild.innerHTML = `${response.data.surprisingCount}`
}

const onClickReCommentFunnyButton = async (postId, commentId, recommentId) => {
    const recomment_funny_button = document.getElementById(`${recommentId}-recomment-funny-button`)
    const response = await axios.post(`/community/posts/${postId}/comments/${commentId}/recomments/${recommentId}/recommentEmotion/funny/`)
    recomment_funny_button.firstElementChild.innerHTML = `${response.data.funnyCount}`
}

const makeRecommentBox = (postId, commentId) => {
    const recomment_list = document.getElementById(`${commentId}-recomment-list`)
    let csrf = document.createElement('input');
    csrf.setAttribute("type","hidden");
    csrf.setAttribute("name","_token");
    csrf.setAttribute("value","{{csrf_field()}}");
 
    
    let replyinput = document.createElement('input');
    replyinput.setAttribute('id', `${commentId}-recomment-input`);
    replyinput.setAttribute('type', 'text');
    replyinput.setAttribute('name', 'content');

    let submit_button = document.createElement('button');
    submit_button.setAttribute('onclick', `onAddReComment(${postId}, ${commentId})`);
    submit_button.innerHTML = '대댓글 달기';
  

    recomment_list.appendChild(csrf);
    recomment_list.appendChild(replyinput);
    recomment_list.appendChild(submit_button);
}