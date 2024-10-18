from extractors.web import html2text, markdown2text
from textwrap import dedent

def describe_html2text() -> None:
  def it_works() -> None:
    html = c("""
      text11
      text12
      <p>
        text21
        text22
      </p>
      <div>
        <div>text3</div>
      </div>
      <a href="https://url1.com">text4</a>
      <img src="something" alt="text5"/>
      
      <a href="https://url2.com"><img/> text6</a>
      <!-- text7 -->

      <code>
        console.log('💚')
      </code>
    """)
    text = c("""
      text11
      text12
      
      text21
        text22
      
      text3
      
      Text4: https://url1.com
      
      Text6: https://url2.com
      
      /Code/
    """)
    assert html2text(html) == dedent(text).strip()

def describe_markdown2text() -> None:
  def it_works1() -> None:
    md = c("""
      First 🧡
      ```js
      console.log('foo')
      ```
      Second 💚
    """)
    text = c("""
      First 🧡
      
      /Code/
      
      Second 💚
    """)
    assert markdown2text(md) == text

  def it_works2() -> None:
    md = c("""
      <a href="mailto:test1@gmail.com"><img src="https://svg.herokuapp.com"/></a>
      <a href="mailto:test2@gmail.com">test2</a>
      <a href="https://test3.com">test3</a>
      
      [![alt](https://svg.herokuapp.com)](mailto:test4@gmail.com)
      [![](https://svg.herokuapp.com)](mailto:test5@gmail.com)
      [test6](mailto:test6@gmail.com)
      [test7](https://test7.com)
    """)
    text = c("""
      Email: mailto:test1@gmail.com

      Test2: mailto:test2@gmail.com
      
      Test3: https://test3.com
      
      Email: mailto:test4@gmail.com
      
      Email: mailto:test5@gmail.com
      
      Test6: mailto:test6@gmail.com
      
      Test7: https://test7.com
    """)
    assert markdown2text(md) == text

  def it_works3() -> None:
    md = c("""
      <div align=center>
        <a href="https://github.com/Sabya-Sachi-Seal">
          <img src="https://raw.githubcontent.com/Sabya-Sachi-Seal/Sabya-Sachi-Seal/divider.gif">
        </a>
      </div>
      <a href="https://toptal.com/resume/xxx">
        <img src="foobar"/>
      </a>
      <a href="https://unknown-site.com">
        <img src="foobar"/>
      </a>  
    """)
    text = c("""
      URL: https://github.com/Sabya-Sachi-Seal
      
      URL: https://toptal.com/resume/xxx
      
      /URL/
    """)
    assert markdown2text(md) == text

def c(text: str) -> str:
  return dedent(text).strip()
