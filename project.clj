(defproject finchest-explore "0.1.0-SNAPSHOT"
  :dependencies [[org.clojure/clojure "1.8.0"]
                 [org.clojure/clojurescript "1.9.293"]
                 [reagent "0.6.0"]
                 [binaryage/devtools "0.8.3"]
                 [re-frisk "0.3.2"]
                 [cljs-ajax "0.5.8"]
                 [re-com "1.2.0"]
                 [funcool/cuerdas "2.0.2"]
                 [json-html "0.4.0"]
                 [alandipert/storage-atom "2.0.1"]
                 [com.andrewmcveigh/cljs-time "0.4.0"]
                 [medley "0.8.4"]
                 [com.rpl/specter "0.13.2"]
                 [cljsjs/filesaverjs "1.3.3-0"]]

  :min-lein-version "2.5.3"

  :source-paths ["src/clj"]

  :plugins [[lein-cljsbuild "1.1.5"]]

  :clean-targets ^{:protect false} ["resources/public/js/compiled"
                                    "target"
                                    "test/js"]

  :figwheel {:css-dirs ["resources/public/css"]
             :server-port 3450}


  :repl-options {:nrepl-middleware [cemerick.piggieback/wrap-cljs-repl]}

  :profiles
  {:dev
   {:dependencies [
                   [figwheel-sidecar "0.5.8"]
                   [com.cemerick/piggieback "0.2.1"]]

    :plugins      [[lein-figwheel "0.5.8"]
                   [lein-doo "0.1.7"]
                   [cider/cider-nrepl "0.14.0"]
                   [lein-cljfmt "0.5.6"]]}}

  :cljsbuild
  {:builds
   [{:id           "dev"
     :source-paths ["src/cljs"]
     :figwheel     {:on-jsload "finchest-explore.core/reload"}
     :compiler     {:main                 finchest-explore.core
                    :optimizations        :none
                    :output-to            "resources/public/js/compiled/app.js"
                    :output-dir           "resources/public/js/compiled/out"
                    :asset-path           "js/compiled/out"
                    :source-map-timestamp true}}

    {:id           "min"
     :source-paths ["src/cljs"]
     :compiler     {:main            finchest-explore.core
                    :optimizations   :advanced
                    :parallel-build  true
                    :output-to       "resources/public/js/compiled/app.js"
                    :closure-defines {goog.DEBUG false}
                    :pretty-print    false}}

    {:id           "test"
     :source-paths ["src/cljs" "test/cljs"]
     :compiler     {:output-to     "resources/public/js/compiled/test.js"
                    :output-dir    "resources/public/js/compiled/test/out"
                    :main          finchest-explore.runner
                    :optimizations :none}}]})
