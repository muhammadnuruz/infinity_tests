import {u as n, r as m, j as e, L as i, s as c} from "./index-4xg0ltYw.js";
import {u} from "./usePost-ARu01beh.js";
const p = ()=>{
    const s = n()
      , [a,t] = m.useState({
        password: "",
        full_name: ""
    })
      , {mutate: l} = u({
        queryKey: "users",
        onError: ()=>{}
        ,
        path: "/auth/token/",
        onSuccess: r=>{
            const d = {
                fullName: a.full_name,
                values: r
            };
            c.set("token", d),
            s("/")
        }
    })
      , o = r=>{
        r.preventDefault(),
        l(a)
    }
    ;
    return e.jsx("section", {
        className: "bg-gray-50 dark:bg-gray-900",
        children: e.jsx("div", {
            className: "flex flex-col items-center justify-center px-6 py-8 mx-auto h-screen lg:py-0",
            children: e.jsx("div", {
                className: "w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700",
                children: e.jsxs("div", {
                    className: "p-6 space-y-4 md:space-y-6 sm:p-8",
                    children: [e.jsx("h1", {
                        className: "text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl dark:text-white text-center",
                        children: "Sign in to your account"
                    }), e.jsxs("form", {
                        action: "#",
                        className: "space-y-4 md:space-y-6",
                        onSubmit: r=>o(r),
                        children: [e.jsxs("div", {
                            className: "form-box",
                            children: [e.jsx("label", {
                                htmlFor: "full-name",
                                className: "block mb-2 text-sm font-medium text-gray-900 dark:text-white",
                                children: "Full name"
                            }), e.jsx("input", {
                                required: !0,
                                type: "text",
                                id: "full-name",
                                name: "fullName",
                                placeholder: "John Doe",
                                value: a.full_name,
                                onChange: r=>{
                                    t({
                                        ...a,
                                        full_name: r.target.value
                                    })
                                }
                                ,
                                className: "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                            })]
                        }), e.jsxs("div", {
                            className: "form-box",
                            children: [e.jsx("label", {
                                htmlFor: "password",
                                className: "block mb-2 text-sm font-medium text-gray-900 dark:text-white",
                                children: "Password"
                            }), e.jsx("input", {
                                required: !0,
                                id: "password",
                                type: "password",
                                name: "password",
                                placeholder: "••••••••",
                                value: a.password,
                                onChange: r=>{
                                    t({
                                        ...a,
                                        password: r.target.value
                                    })
                                }
                                ,
                                className: "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                            })]
                        }), e.jsx("button", {
                            type: "submit",
                            className: "w-full text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800",
                            children: "Sign in"
                        }), e.jsxs("div", {
                            className: "flex items-center justify-between",
                            children: [e.jsxs("p", {
                                className: "text-sm font-light text-gray-500 dark:text-gray-400",
                                children: ["Don’t have an account yet?", " "]
                            }), e.jsx(i, {
                                to: "/pages/registration",
                                className: "text-sm font-medium text-primary-600 hover:underline dark:text-primary-500",
                                children: "Sign up"
                            })]
                        })]
                    })]
                })
            })
        })
    })
}
;
export {p as default};
