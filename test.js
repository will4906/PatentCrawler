/**
 * Created by will on 2017/3/21.
 */

document.getElementById("IVDB007select").firstElementChild.firstElementChild.innerHTML = ">=";

document.getElementById("IVDB007select").firstElementChild.firstElementChild.click();
document.getElementById("IVDB007select").firstElementChild.childNodes[2].childNodes[0].firstElementChild.className = "";
document.getElementById("IVDB007select").firstElementChild.childNodes[2].childNodes[2].firstElementChild.className = "active";

document.getElementById("IVDB007select").firstElementChild.firstElementChild.click();
document.getElementById("IVDB007select").firstElementChild.childNodes[2].childNodes[2].firstElementChild.click();
document.getElementsByName("titleHidden").item(0).attributes.getNamedItem("value").textContent;
document.getElementsByClassName("item-content-body").item(0).childNodes.item(1).childNodes.item(0);
//删除申请日的脚本
document.getElementsByClassName("item-content-body").item(0).childNodes.item(1).removeChild(document.getElementsByClassName("item-content-body").item(0).childNodes.item(1).childNodes.item(0));

document.getElementsByClassName("item").length;
document.getElementsByClassName("item-header").item(0).childNodes.item(3).childNodes.item(3).textContent;
document.getElementsByClassName("item-content-body").item(1).childNodes.item(3).childNodes.item(0).textContent;
document.getElementsByClassName("item-content-body").item(1).childNodes.item(3).removeChild(document.getElementsByClassName("item-content-body").item(1).childNodes.item(3).childNodes.item(0));
document.getElementsByClassName("item-content-body").item(1).childNodes.item(7).childNodes.item(1).textContent;
document.getElementsByClassName("item-content-body").item(1).childNodes.item(7).removeChild(document.getElementsByClassName("item-content-body").item(1).childNodes.item(7).childNodes.item(0));

document.getElementsByClassName("item-content-body").item(1).childNodes.item(11).removeChild(document.getElementsByClassName("item-content-body").item(1).childNodes.item(11).childNodes.item(1));
document.getElementsByClassName("item-content-body").item(1).childNodes.item(11).childNodes.item(1).textContent;

document.getElementsByClassName("item-content-body").item(0).childNodes.item(11).childNodes.item(1).ownerDocument.getElementsByClassName("in-bl").length;
document.getElementsByClassName("item-content-body").item(0).childNodes.item(13).innerText;
document.getElementsByClassName("item-content-body").item(0).ownerDocument

// 点击法律信息按钮，执行后需等待一会
document.getElementsByClassName("item-footer").item(0).childNodes.item(1).childNodes.item(3).click();
// 法律信息节点个数
document.getElementById("lawResult").getElementsByTagName("td").length;
// 法律信息
document.getElementById("lawResult").getElementsByTagName("td").item(document.getElementById("lawResult").getElementsByTagName("td").length - 1).innerText;
// 关闭法律信息框
document.getElementsByClassName("ui-dialog-close").item(0).click();

//#search_result > div.re-content.search-mode-content > div.re-page > div > div > div > div > p:nth-child(10)
////*[@id="search_result"]/div[4]/div[2]/div/div/div/div/p[1]
document.getElementsByClassName("page_top").item(0).childNodes.item(document.getElementsByClassName("page_top").item(0).childNodes.length - 1);
document.getElementsByClassName("page_top").item(0).childNodes.length;
document.getElementsByClassName("page_top").item(0).removeChild(document.getElementsByClassName("page_top").item(0).childNodes.item(0));