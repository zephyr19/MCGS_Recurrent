//鱼眼缩放辅助函数1
function d3_fisheye_scale(scale, d, a) {
    function fisheye(_) {
        var x = scale(_),
            left = x < a,
            v,
            range = d3.extent(scale.range()),
            min = range[0],
            max = range[1],
            m = left ? a - min : max - a;
        if (m == 0) m = max - min;
        return (left ? -1 : 1) * m * (d + 1) / (d + (m / Math.abs(x - a))) + a;
    }

    fisheye.distortion = function (_) {
        if (!arguments.length) return d;
        d = +_;
        return fisheye;
    };

    fisheye.focus = function (_) {
        if (!arguments.length) return a;
        a = +_;
        return fisheye;
    };

    fisheye.copy = function () {
        return d3_fisheye_scale(scale.copy(), d, a);
    };

    fisheye.nice = scale.nice;
    fisheye.ticks = scale.ticks;
    fisheye.tickFormat = scale.tickFormat;

    return rebind(fisheye, scale, "domain", "range");
}

//鱼眼辅助函数2
function rebind(e, t) {
    var n = 1, r = arguments.length, i;
    while (++n < r)
        e[i = arguments[n]] = a(e, t, t[i]);
    return e
}

//鱼眼组件对象
export default {
    scale: function (scaleType) {
        return d3_fisheye_scale(scaleType(), 3, 0);
    },
    circular: function () {
        var radius = 200,
            distortion = 2,
            k0,
            k1,
            focus = [0, 0];

        function fisheye(d) {
            var dx = d.cx - focus[0],
                dy = d.cy - focus[1],
                dd = Math.sqrt(dx * dx + dy * dy);
            if (!dd || dd >= radius) return { x: d.cx, y: d.cy, z: 1 };
            var k = k0 * (1 - Math.exp(-dd * k1)) / dd * .75 + .25;
            return {
                x: focus[0] + dx * k,
                y: focus[1] + dy * k,
                z: Math.min(1, 10)
            };
        }

        function rescale() {
            k0 = Math.exp(distortion);
            k0 = k0 / (k0 - 1) * radius;
            k1 = distortion / radius;
            return fisheye;
        }

        fisheye.radius = function (_) {
            if (!arguments.length) return radius;
            radius = +_;
            return rescale();
        };
        fisheye.distortion = function (_) {
            if (!arguments.length) return distortion;
            distortion = +_;
            return rescale();
        };
        fisheye.focus = function (_) {
            if (!arguments.length) return focus;
            focus = _;
            return fisheye;
        };
        return rescale();
    }
};
