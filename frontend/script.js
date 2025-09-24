async function analyzeCode() {
  const codeInput = document.getElementById("code-input").value.trim();
  const fileInput = document.getElementById("file-input").files[0];
  const resultsDiv = document.getElementById("results");
  const loadingDiv = document.getElementById("loading");
  const analyzeBtn = document.getElementById("analyze-btn");

  // 清空上次结果
  resultsDiv.style.display = "none";
  resultsDiv.innerHTML = "";

  // 验证输入
  if (!codeInput && !fileInput) {
    alert("请粘贴代码或上传文件！");
    return;
  }

  // 显示加载状态
  loadingDiv.style.display = "block";
  analyzeBtn.disabled = true;
  analyzeBtn.textContent = "检测中...";

  try {
    const formData = new FormData();
    if (fileInput) {
      formData.append("file", fileInput);
    } else {
      formData.append("code", codeInput);
    }

    const response = await fetch("http://127.0.0.1:8000/api/detect", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (data.error) {
      resultsDiv.innerHTML = `<p style="color:red">❌ ${data.error}</p>`;
    } else if (data.data && data.data.issues && data.data.issues.length > 0) {
      let issuesHtml = "<h2>🔴 检测到问题</h2>";
      data.data.issues.forEach((issue) => {
        issuesHtml += `
          <div class="issue">
            <h3>[${issue.rule_id || 'N/A'}] ${issue.message}</h3>
            <p><strong>严重等级：</strong>${issue.severity || '中'}</p>
            <p class="suggestion">💡 ${issue.suggestion}</p>
          </div>
        `;
      });
      resultsDiv.innerHTML = issuesHtml;
    } else {
      resultsDiv.innerHTML = "<h2>✅ 恭喜！未发现代码规范问题</h2>";
    }

    resultsDiv.style.display = "block";
  } catch (err) {
    resultsDiv.innerHTML = `<p style="color:red">❌ 请求失败：${err.message}</p>`;
    resultsDiv.style.display = "block";
    console.error(err);
  } finally {
    loadingDiv.style.display = "none";
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "🚀 开始检测";
  }
}