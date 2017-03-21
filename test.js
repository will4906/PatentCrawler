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