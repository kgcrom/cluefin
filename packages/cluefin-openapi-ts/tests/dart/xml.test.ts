import { describe, expect, it } from 'vitest';

import { parseFlatXmlList, parseXmlStatus } from '../../src/dart/xml';

describe('parseFlatXmlList', () => {
  it('list 항목의 자식 태그를 맵으로 만들고 엔티티·CDATA·빈 태그를 처리한다', () => {
    const xml = `<?xml version="1.0" encoding="UTF-8"?>
<result>
  <list>
    <corp_code>00126380</corp_code>
    <corp_name>삼성전자 &amp; 계열 &#44032;&#x1F600;</corp_name>
    <stock_code>005930</stock_code>
    <modify_date>20240101</modify_date>
  </list>
  <list>
    <corp_code>00000001</corp_code>
    <corp_name><![CDATA[A<B>]]></corp_name>
    <stock_code> </stock_code>
    <corp_eng_name/>
  </list>
</result>`;

    expect(parseFlatXmlList(xml)).toEqual([
      { corp_code: '00126380', corp_name: '삼성전자 & 계열 가😀', stock_code: '005930', modify_date: '20240101' },
      { corp_code: '00000001', corp_name: 'A<B>', stock_code: '', corp_eng_name: '' },
    ]);
  });

  it('항목이 없으면 빈 배열', () => {
    expect(parseFlatXmlList('<result><status>000</status></result>')).toEqual([]);
  });
});

describe('parseXmlStatus', () => {
  it('에러 본문에서 status/message 를 읽는다', () => {
    expect(parseXmlStatus('<result><status>014</status><message>파일이 존재하지 않습니다.</message></result>')).toEqual(
      {
        status: '014',
        message: '파일이 존재하지 않습니다.',
      },
    );
  });

  it('status 가 없으면 undefined', () => {
    expect(parseXmlStatus('<document><body>x</body></document>')).toBeUndefined();
  });
});
