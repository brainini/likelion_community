const getCommentElement = (content, postId, commentId, author, created_at) => {
	
    let newCommentDiv = document.createElement('div');
    newCommentDiv.setAttribute('id',`${commentId}-comment`);
    let newCommentElement = document.createElement('p');
    newCommentElement.innerHTML = `${author}: ${content} &nbsp; &nbsp;${created_at} &nbsp;`;
      
    let likeButton = document.createElement('a');
    likeButton.setAttribute('onclick', `onClickCommentLike(${postId},${commentId})`);
    likeButton.setAttribute('id', `${commentId}-comment-like-button`);
    likeButton.innerHTML = "0 Likes";
    let deleteButton = document.createElement('a');
    deleteButton.setAttribute('onclick', `onClickCommentDelete(${postId},${commentId})`);
    deleteButton.innerHTML = " 댓글 삭제"
  
    newCommentElement.appendChild(likeButton);
    newCommentElement.appendChild(deleteButton);
    newCommentDiv.appendChild(newCommentElement);
    
    recomment_list = document.createElement('div');
    recomment_list.setAttribute('id', `${commentId}-recomment-list`)
    newCommentDiv.appendChild(recomment_list);

    let csrf = document.createElement('input');
    csrf.setAttribute("type","hidden");
    csrf.setAttribute("name","_token");
    csrf.setAttribute("value","{{csrf_field()}}");
    recomment_list.appendChild(csrf);
    
    let replyinput = document.createElement('input');
    replyinput.setAttribute('id', `${commentId}-recomment-input`);
    replyinput.setAttribute('type', 'text');
    replyinput.setAttribute('name', 'content');
    recomment_list.appendChild(replyinput);
    let submit_button = document.createElement('button');
    submit_button.setAttribute('onclick', `onAddReComment(${postId}, ${commentId})`);
    submit_button.innerHTML = '대댓글 달기';
    recomment_list.appendChild(submit_button);
    

    
    return newCommentDiv; 
}
  
const onAddComment = async (postId) => {
    const commentInputElement = document.getElementById("comment-input");
    if(commentInputElement.value) {
        // axios로 보내줄 data Form을 만들어 줍니다. 
        let data = new FormData();
        // content라는 key를 만들고, tag input 값을 적어줍니다. 
        data.append("content", commentInputElement.value);
        console.log(data);
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
        const recommentElement = getReCommentElement(recommentInputElement.value, postId, response.data.recommentId, response.data.author, response.data.created_at);
        document.getElementById(`${commentId}-recomment-list`).appendChild(recommentElement);
        recommentInputElement.value="";
        const commentCount = document.getElementById('comment-count');
        commentCount.innerHTML = `<strong>댓글이 ${response.data.commentCount}개 있습니다</strong>`;
    }
}