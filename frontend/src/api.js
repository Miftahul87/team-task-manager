const BASE=import.meta.env.VITE_API_URL||'http://localhost:8000/api'
let access=localStorage.getItem('access')
let refresh=localStorage.getItem('refresh')
export function saveTokens(a,r){access=a;refresh=r;localStorage.setItem('access',a);localStorage.setItem('refresh',r)}
export function clearTokens(){access=null;refresh=null;localStorage.removeItem('access');localStorage.removeItem('refresh')}
export async function api(path,options={}){
  const headers={'Content-Type':'application/json',...(options.headers||{})}
  if(access) headers.Authorization=`Bearer ${access}`
  let response=await fetch(`${BASE}${path}`,{...options,headers})
  if(response.status===401&&refresh&& !path.includes('/auth/token')){
    const rr=await fetch(`${BASE}/auth/token/refresh/`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({refresh})})
    if(rr.ok){const data=await rr.json();saveTokens(data.access,data.refresh||refresh);headers.Authorization=`Bearer ${data.access}`;response=await fetch(`${BASE}${path}`,{...options,headers})}
    else clearTokens()
  }
  const data=response.status===204?null:await response.json().catch(()=>({}))
  if(!response.ok) throw new Error(data.detail||JSON.stringify(data)||'Request failed')
  return data
}
