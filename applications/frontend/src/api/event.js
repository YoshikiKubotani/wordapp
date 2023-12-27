class _EventApi {
  static async _request({url, method, body = undefined, customHeaders = {}, queryParams = {}}) {
    const backend_url = process.env.BACKEND_API_URL ?? 'http://localhost:8000';
    const queryString = this._encodeQueryParams(queryParams);
    const fullUrl = `${backend_url}${url}${queryString}`;
    let headers = {
      "Content-Type": "application/json",
      ...customHeaders
    };

    let response;
    try {
      response = await fetch(`${fullUrl}`, {
        method: method,
        headers: headers,
        body: body ? JSON.stringify(body) : null,
        // credentials: 'include',  // 必要に応じて追加
      });

      // HTTPステータスコードのチェック
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Unknown error');
      }

    } catch (error) {
      console.error("API request failed:", error);
      throw error;
    }

    return response.json();
  }
  static _encodeQueryParams(params) {
    const pairs = [];
    for (const key in params) {
      if (params.hasOwnProperty(key)) {
        const value = params[key];
        pairs.push(`${encodeURIComponent(key)}=${encodeURIComponent(value)}`);
      }
    }
    return pairs.length ? `?${pairs.join('&')}` : '';
  }

  static makeTest(gradeId, numItems) {
    // テストを作成するためのAPI
    return this._request({
      url: `/tests/${gradeId}`,
      method: 'GET',
      queryParams: {num: numItems}
    })
  }

  static getItemInfo(itemUuid) {
    // 次の問題を取得するためのAPI
    return this._request({
      url: `/items/${itemUuid}`,
      method: 'GET'
    })
  }

  static getItemAnswer(itemUuid) {
    // 現在の問題の答えを取得するためのAPI
    return this._request({
      url: `/items/${itemUuid}/answer`,
      method: 'GET'
    })
  }

  static checkUserResponse(itemUuid, userResponse) {
    // ユーザーの回答を送信するためのAPI
    return this._request({
      url: `/items/${itemUuid}/response`,
      method: 'POST',
      body: userResponse
    })
  }

}

export const EventApi = _EventApi