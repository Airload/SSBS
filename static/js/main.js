
    function toggleElement(elementToShow) {
    // 순차적으로 모든 요소를 숨김 처리
    for (let i = 1; i <= 5; i++) {
      let currentElement = document.getElementById('element' + i);
      currentElement.classList.add('hidden');
    }

    // 선택한 요소만 나타나도록 함
    let selectedElement = document.getElementById('element' + elementToShow);
    selectedElement.classList.remove('hidden');
  }
  
  function moveToAnotherPage(element) {
    // 클릭한 요소의 data-page 속성을 읽어옵니다.
    var pageNumber = element.getAttribute("data-page");

    // 페이지 번호에 따라 이동할 경로를 지정합니다.
    var destination;

    switch (pageNumber) {
      case 'page1':
        destination = "{% url 'map' %}";
        break;
      case 'page2':
        destination = "{% url 'data' %}";
        break;
      case 'page3':
        destination = "{% url 'report' %}";
        break;
      default:
        // 기본적으로 어떤 페이지로 이동할지 정의할 수 있습니다.
    }

    // 실제로 이동합니다.
    window.location.href = destination;
    
  }
  function goLink(url) {
    // 창의 너비와 높이를 원하는 값으로 조절
    var windowWidth = 1280;
    var windowHeight = 960;

    // 창을 중앙에 위치시키기 위한 좌표 계산
    var windowLeft = (window.screen.width - windowWidth) / 2;
    var windowTop = (window.screen.height - windowHeight) / 2;

    // 새 창 열기
    window.open(url, '_blank', 'width=' + windowWidth + ', height=' + windowHeight + ', left=' + windowLeft + ', top=' + windowTop);
  }