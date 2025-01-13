/*
prosa
Copyright (C) 2024  Henric Zazzi <hzazzi@kth.se>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
//-----------------------------------------------------------------------
function navigateToUrl(baseurl, dropdown) {
    const url = baseurl + dropdown.value;

    if (url) {
        window.location.href = url;
        }
    }
//-----------------------------------------------------------------------
function openWindowAtPointer(event, baseurl, url) {
    const pointerX = event.screenX;
    const pointerY = event.screenY;
    const width = 200;
    const height = 450;
    popup = window.open(
        url + window.location.search,
        '_blank',
        `width=${width},height=${height},left=${pointerX},top=${pointerY},toolbar=no,scrollbars=no,resizable=no`
        );
    if (popup) {
        popup.onblur = function () {
            popup.close();
            };
        }
    window.addEventListener('message', (e) => {
        if (e.origin === window.location.origin) {
            console.log('Selected items received from child:', e.data);
            const selectedItems = e.data.join(',');
            const redirectUrl = baseurl+selectedItems;
            window.location.href = redirectUrl;
            }
        });
    }
//-----------------------------------------------------------------------
function sendSelectedItemsToParent(elementid) {
    const selectBox = document.getElementById(elementid);
    const selectedOptions = Array.from(selectBox.selectedOptions).map(option => option.value);

    if (window.opener) {
        window.opener.postMessage(selectedOptions, window.location.origin);
        window.close();
        }
    else {
        alert('No parent window found.');
        }
    }
//-----------------------------------------------------------------------
